import abc
import json
import httpx
from time import sleep


class BaseScrapeDigi(abc.ABC):
    def __init__(
        self,
        client: httpx.Client,
        main_url,
        detail_url,
        final_dkp
    ):
        self.main_url = main_url
        self.detail_url = detail_url
        self.client = client
        self.final_dkp = final_dkp
        self.results = list()

    abc.abstractmethod
    def get_number_of_pages(self):
        pass

    abc.abstractmethod
    def get_page_product(self, page):
        pass
        
    abc.abstractmethod
    def get_detail(self, dkp, title):
        pass

    abc.abstractmethod
    def gather_items(self):
        pass


class ScrapeDigi(BaseScrapeDigi):
    
    def get_number_of_pages(self):
        page = self.client.get(
            self.main_url
        )
        num_of_pages = page.json().get("data").get("pager").get("total_pages")
        return num_of_pages

    def get_page_product(self, page):
        print(f"This is page number: {page}")
        page_url = self.main_url + f"&page={page}"
        res = self.client.get(
            page_url
        )
        products = res.json().get("data").get("products")
        dkps = [item.get("id") for item in products]
        titles = [item.get("title_fa") for item in products]
        results = list()
        index = 1
        finished = False
        for dkp, title in zip(dkps, titles):
            print(index)
            result = self.get_detail(dkp, title)
            results.append(result)
            sleep(0.2)
            index += 1
            if str(dkp) == str(self.final_dkp):
                finished = True
                return results, finished

        return results, finished

    def get_detail(self, dkp, title):
        final_url = f"{self.detail_url}/{dkp}/"
        resp = self.client.get(
            final_url
        )
        variants = resp.json().get("data").get("product").get("variants")
        brand = resp.json().get("data").get("product").get("brand")
        results = {
            "dkp": dkp,
            "title": title,
            "product": variants,
            "brand": brand
        }
        # print(results)
        return results

    def gather_items(self):
        pages = self.get_number_of_pages()
        start_page = 1
        try:
            for page in range(start_page, 10000):
                result, finished = self.get_page_product(page)
                self.results.extend(result)
                if finished:
                    return self.results
                sleep(0.2)
            return self.results
        except:
            return self.results


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def scrape_data(main_url, detail_url, final_dkp, filename):
    with httpx.Client() as client:
        scraper = ScrapeDigi(
            client=client,
            main_url=main_url,
            detail_url=detail_url,
            final_dkp=final_dkp
        )
        data = scraper.gather_items()
    save_json(data, filename)

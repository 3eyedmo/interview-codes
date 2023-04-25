import glob
from create_excel import create_analyze_excel



dirs = glob.glob("data/1401-11-09/*.json")

for d in dirs:
    print(d)
    create_analyze_excel(d)

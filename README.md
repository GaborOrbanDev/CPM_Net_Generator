# Minimális méretű projektháló generátor

### CLI alkalmazás paraméterei:
```
optional arguments:
  -h, --help            show this help message and exit
  -f FILE_NAME, --file_name FILE_NAME
                        Megadhatja a beolvasandó excel file nevét / elérési útját. Alapértelmezett esetben a programmal egy     
                        mappában lévő activity_input.xlsx filet fogja keresni
```

### Bemenetként megadott xlsx file elvárt struktúrája
- <b>ActivityID</b>: tevékenység azonosítója, ez a változó lesz megjelenítve a projektháló élein
- <b>ActivityName</b>: tevékenység neve, opcionális változó
- <b>Duration</b>: tevékenység hossza
- <b>Requirements</b>: tevékenység előkövetelménye(i), vesszővel elválasztott felsorolása az `ActivityID`-(k)nak

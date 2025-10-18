# 🎪 Cirku galdu spēļu programma

Šī ir Python programmā izstrādāta interaktīva cirka spēle, kurā spēlētāji var izveidot savu cirka grupu, sacensties dažādās aktivitātēs un sekot līdzi rezultātiem. Spēle izmanto Tkinter GUI, lai nodrošinātu vieglu un vizuāli saprotamu lietotāja saskarni.

## Funkcionalitāte

- **👤Spēlētāju Izveide**

  Lietotāji var izvēlēties spēlētāju skaitu un piešķirt katram vārdu.
  
  Spēlētāju statistika tiek glabāta un atjaunināta spēles gaitā.

  ![image](https://github.com/user-attachments/assets/2c954993-22aa-4d41-8aad-c96fbf489e91)
  
- **🎲Spēles Mehānika**

  Spēlētāji sacenšas, veicot dažādas cirka aktivitātes, metot kauliņu un sekojot līdzi savu kauliņa iegūtajai vietai.
  
  Ir iekļauti gadījuma notikumi un īpašas situācijas, piemēram, papildu metieni vai kāpšana uz trepītēm.

  ![image](https://github.com/user-attachments/assets/7e317a03-1975-4c9a-a7df-224cb0e43713)
  
- **🖥️Grafiskā Saskarne (GUI)**  

  Draudzīgs interfeiss ar pogām, logiem un teksta laukiem.
  
  Spēlētāji redz savu pozīciju, rezultātus un kauliņa metienu kārtu.
  
  Rezultātu logs un žurnāls ļauj viegli sekot spēles gaitu.

- **🏆Turnīra režīms**  

  Spēlētāji tiek sadalīti divās grupās, un uzvarētāji no katras grupas cīnās finālā.
  
  Sistēma automātiski seko līdzi finālistiem un diskvalificētajiem spēlētājiem.

  ![image](https://github.com/user-attachments/assets/5ffec5a1-0c2d-4302-9c2a-9a8c8f9d4696)
  ![image](https://github.com/user-attachments/assets/c1bdca9f-d9bc-4af0-b6e7-4e75e16c5c74)
  
- **📄Datu Glabāšana**
  
  Visi spēlētāju dati tiek saglabāti teksta failā, kas ļauj viegli pārvaldīt un pārbaudīt saglabāto informāciju.

  ![image](https://github.com/user-attachments/assets/b0517310-a250-483a-88d3-30a02e0c9ef5)
  ![image](https://github.com/user-attachments/assets/7ee5806b-0bb1-457a-97d6-22b498e96f0d)

## Sistēmas Sastāvdaļas
- **Python Kods**
  
  Projekts sadalīts trīs galvenajos moduļos:
 
  gDarbs_spele.py – galvenā klase, kas satur spēles loģiku.
 
  spele_gui.py – klase, kas nodrošina lietotāja saskarni un logus.
 
  spele_metodes.py – klase, kurā ir spēles funkcijas, animācijas un palīdzības metodes.
 
- **Datu Fails**
  
  Teksta failu sistēma, kas saglabā:

  Spēlētaju informāciju (piemēram, lietotājvārds, izspēlētas spēles, uzvaras)

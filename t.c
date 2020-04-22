#define MAX_TITKOS 8092
#define OLVASAS_BUFFER 256
#define KULCS_MERET 5
#define _GNU_SOURCE

#include <stdio.h>
#include <unistd.h>
#include <string.h>


/*  
 *  Clean Code verzió: Bogacsovics Gergő
 *  Tutor: Vincze Tamás Zoltán
 *
 */

/* Átlagos szóhossz kiszámítása. */
double
atlagos_szohossz (const char *titkos, int titkos_meret)
{
  /* sz jelöli a szóközök számát */
  int sz = 0;
  for (int i = 0; i < titkos_meret; ++i)
    if (titkos[i] == ' ')
      ++sz;
  
  /* Visszatéréi érték: elosztjuk a hosszt a szóközök számával. Így megkapjuk az átlagos szóhosszt. */
  return (double) titkos_meret / sz;
}

/* Megvizsgáljuk, tiszta-e a szöveg. */
int
tiszta_lehet (const char *titkos, int titkos_meret)
{
  // a tiszta szoveg valszeg tartalmazza a gyakori magyar szavakat
  // illetve az átlagos szóhossz vizsgálatával csökkentjük a
  // potenciális töréseket

  double szohossz = atlagos_szohossz (titkos, titkos_meret);

  return szohossz > 6.0 && szohossz < 9.0
    && strcasestr (titkos, "hogy") && strcasestr (titkos, "nem")
    && strcasestr (titkos, "az") && strcasestr (titkos, "ha");

}

/* exor végrehajtása */ 
void
exor (const char kulcs[], int kulcs_meret, char titkos[], int titkos_meret)
{

  int kulcs_index = 0;

  for (int i = 0; i < titkos_meret; ++i)
    {

      /* Bájtonként végrehajtjuk az XOR műveletet.                          * 
       * A % segítségével érjük el, hogy a kulcs mindig aktuális maradjon, akkor is, ha a szöveg hosszabb mint a kulcs(legtöbb esetben ez teljesül) */
      titkos[i] = titkos[i] ^ kulcs[kulcs_index];
      kulcs_index = (kulcs_index + 1) % kulcs_meret;

    }

}

/* exor törés végrehajtása. */
int
exor_tores (const char kulcs[], int kulcs_meret, char titkos[],
      int titkos_meret)
{

  exor (kulcs, kulcs_meret, titkos, titkos_meret);

  return tiszta_lehet (titkos, titkos_meret);

}

int
main (void)
{
  int teszt[20]={'a','b','c','d','e','f','g','h','i','j','0','1','2','3','4','5','6','7','8','9'};
  
  char kulcs[KULCS_MERET];
  char titkos[MAX_TITKOS];
  char *p = titkos;
  int olvasott_bajtok;

  // titkos fajt berantasa
  /* Amíg tudunk olvasni a bemenetről, addig végrehajtódik a ciklus. Ha már nincs több adat, amit beolvashatnánk, a read 0 értéket ad vissza, és a ciklus véget ér. */
  /* man read -> read kézikönyve további információért */
  while ((olvasott_bajtok =
    read (0, (void *) p,
    (p - titkos + OLVASAS_BUFFER <
     MAX_TITKOS) ? OLVASAS_BUFFER : titkos + MAX_TITKOS - p)))
    p += olvasott_bajtok;

  // maradek hely nullazasa a titkos bufferben  
  for (int i = 0; i < MAX_TITKOS - (p - titkos); ++i)
    titkos[p - titkos + i] = '\0';

  // osszes kulcs eloallitasa
  /* Ezt for ciklusokkal érük el. Így minden lehetséges kulcs előáll, azokat "csak" ki kell próbálni. */
  for (int i=0; i<sizeof(teszt); i++)
  {
    int ii=teszt[i];
    for (int j=0; j<sizeof(teszt); j++)
    {
      int ji=teszt[j];
      for (int k = 0 ; k<sizeof(teszt); k++)
      {
        int ki=teszt[k];
        for (int l = 0 ; l<sizeof(teszt); l++)
        {
          int li=teszt[l];
          for (int m = 0 ; m<sizeof(teszt); m++)
          {
            int mi=teszt[m];
            kulcs[0] = ii;
            kulcs[1] = ji;
            kulcs[2] = ki;
            kulcs[3] = li;
            kulcs[4] = mi;
      
                    /* Ha teljesül az exortörés, akkor kiirjuk az éppen aktuális kulcsot és a tisztaszöveget. */
        if (exor_tores (kulcs, KULCS_MERET, titkos, p - titkos))
          printf
      ("Kulcs: [%c%c%c%c%c]\nTiszta szoveg: [%s]\n",
       ii, ji, ki, li, mi,titkos);

        // ujra EXOR-ozunk, igy nem kell egy masodik buffer  
        exor (kulcs, KULCS_MERET, titkos, p - titkos);
      }
    }
  }

}
  
}

  return 0;
}

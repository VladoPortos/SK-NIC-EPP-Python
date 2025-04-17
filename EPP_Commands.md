EPP príkazy
Príkaz: | <login> | <logout> | <hello> | <poll> | <check> | <create> | <delete> | <info> | <transfer> | <update> | <renew> |

Príkaz <login>
Príkaz <login> sa používa na vytvorenie a overenie spojenia so serverom EPP. Príkaz je totožný s definíciou v RFC.
Príkaz <login> musí byť odoslaný na server pred akýmkoľvek iným príkazom EPP. Spojenie so serverom EPP je ukončené príkazom <logout>.

Prvok <clID>, ktorý obsahuje ID Registrátora.
Prvok <PW>, ktorý obsahuje heslo Registrátora, pričom veľké a malé písmená sa rozlišujú.
Voliteľný prvok <newPW>, ktorý obsahuje nové heslo použiteľné pre nasledovné prihlásenie.
Prvok <options>, ktorý obsahuje podradené prvky.
Prvok <version> , ktorý identifikuje verziu protokolu použitú pre príkaz či prebiehajúce spojenie servera. Podporovaná verzia je 1.0.
Prvok <lang>, ktorý určuje jazykovú verziu textu odozvy, ako aj samotného príkazu alebo prebiehajúceho spojenia so serverom EPP.
Prvok <svcs> obsahuje:
Prvky <objURI> , ktoré obsahujú menný priestor v tvare URI (URI namespace) predstavujúci objekty, ktoré majú byť použité počas spojenia. Podporované objekty: domain, contact, host.
Voliteľný prvok <svcExtension>, ktorý obsahuje prvky epp:extURI identifikujúce rozšírenia objektov v rámci spojenia so serverom.
Príklad príkazu <login>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <login>
         <clID>ClientX</clID>
         <pw>foo-BAR2</pw>
         <newPW>bar-FOO2</newPW>
         <options>
           <version>1.0</version>
           <lang>en</lang>
         </options>
         <svcs>
            <objURI>urn:ietf:params:xml:ns:host-1.0</objURI>
            <objURI>urn:ietf:params:xml:ns:contact-1.0</objURI>
            <objURI>urn:ietf:params:xml:ns:domain-1.0</objURI>
           <svcExtension>
             <extURI>http://www.sk-nic.sk/xml/epp/sk-contact-ident-0.2</extURI>
           </svcExtension>
         </svcs>
       </login>
       <clTRID>ABC-12345</clTRID>
     </command>
   </epp>
Príklad odpovede na <login>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <trID>
      <clTRID>ABC-12345</clTRID>
      <svTRID>54321-XYZ</svTRID>
    </trID>
  </response>
</epp>
Príkaz <logout>
Príkaz < logout > je totožný s definíciou v RFC. Príkaz <logout> sa používa na ukončenie spojenia s EPP serverom. Po prijatí tohto príkazu EPP server odpovie a preruší spojenie s klientom.

<logout> musí byť zadaný ako prázdny prvok a nesmie obsahovať žiadne podradené prvky.

Príklad príkazu <logout>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <logout/>
    <clTRID>ABC-12345</clTRID>
  </command>
</epp>
Príklad odpovede na <logout>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
  <response>
    <result code="1500">
      <msg>
        Command completed successfully; ending session
      </msg>
    </result>
    <trID>
      <svTRID>118073</svTRID>
    </trID>
  </response>
</epp>
Príkaz <hello>
Príkaz <hello> je totožný s definíciou v RFC.
Príkaz <hello> musí byť prázdny a nesmie obsahovať žiadne podradené prvky.
EPP server reaguje na príkaz <hello> alebo na úspešné pripojenie EPP servera s klientom vrátením odpovede <greeting>. Odpoveď <greeting> sa skladá z:

Prvku <svID>, ktorý obsahuje názov EPP servera.
Prvku <svDate>, v ktorom sa uvádza aktuálny dátum a čas servera (v UTC).
Prvku <svcMenu>, ktorý identifikuje služby podporované EPP serverom:
Prvok <version>, ktorý identifikuje verziu protokolu podporovanú EPP serverom. Aktuálna podporovaná verzia je 1.0. V budúcnosti môže server podporovať aj viac verzií, prvok preto môže mať viac výskytov.
Jeden alebo viac prvkov <lang>, ktoré obsahujú identifikátory jazykovej verzie textovej odozvy, ktoré EPP server pozná. Hodnota jazyka má štruktúru definovanú podľa dokumentu [RFC 4646].
Jeden alebo viac prvkov<objURI>, ktoré obsahujú menný priestor v tvare URI pre objekty, ktorých používanie je serverom podporované.
Voliteľný prvok <svcExtension>
Jeden alebo viac prvkov <extURI>, ktoré obsahujú menný priestor v tvare URI pre rozšírenia objektov, ktorých používanie je serverom podporované.
Príklad príkazu <hello>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
 <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <hello/>
</epp>
Odpoveď <greeting> sa posiela v dvoch prípadoch – 1. keď sa vytvorí spojenie a 2. na príkaz <hello>.

Príklad odpovede na <greeting>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <greeting>
    <svID>Example EPP server epp.example.com</svID>
    <svDate>2000-06-08T22:00:00.0Z</svDate>
    <svcMenu>
      <version>1.0</version>
      <lang>en</lang>
      <lang>sk</lang>
      <objURI>urn:ietf:params:xml:ns:host-1.0</objURI>
      <objURI>urn:ietf:params:xml:ns:contact-1.0</objURI>
      <objURI>urn:ietf:params:xml:ns:domain-1.0</objURI>
      <svcExtension>
        <extURI>http://www.sk-nic.sk/xml/epp/sk-contact-ident-0.2</extURI>
      </svcExtension>
    </svcMenu>
   <dcp>
      <access><all/></access>
      <statement>
        <purpose><admin/><prov/></purpose>
         <recipient><ours/><public/></recipient>
        <retention><stated/></retention>
      </statement>
    </dcp>
  </greeting>
</epp>
Príkaz <poll>
Príkaz <poll> sa používa na zobrazenie a získanie notifikácií z fronty servera pre jednotlivých zákazníkov.

Príkaz <poll-op=“req”>
Príkaz sa používa pre získanie najstaršej správy z fronty.

Príklad príkazu <poll-op=“req”>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <poll op="req"/>
       <clTRID>ABC-12345</clTRID>
     </command>
</epp>
Príklad odpovede na tento <poll-op=“req>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <response>
       <result code="1301">
         <msg>Command completed successfully; ack to dequeue</msg>
       </result>
       <msgQ count="5" id="12345">
         <qDate>2000-06-08T22:00:00.0Z</qDate>
         <msg>Transfer requested.</msg>
       </msgQ>
       <resData>
         <obj:trnData
          xmlns:obj="urn:ietf:params:xml:ns:obj-1.0">
           <obj:name>example.com</obj:name>
           <obj:trStatus>pending</obj:trStatus>
           <obj:reID>ClientX</obj:reID>
           <obj:reDate>2000-06-08T22:00:00.0Z</obj:reDate>
           <obj:acID>ClientY</obj:acID>
           <obj:acDate>2000-06-13T22:00:00.0Z</obj:acDate>
           <obj:exDate>2002-09-08T22:00:00.0Z</obj:exDate>
         </obj:trnData>
       </resData>
       <trID>
         <clTRID>ABC-12345</clTRID>
         <svTRID>54321-XYZ</svTRID>
       </trID>
     </response>
</epp>
Príkaz <poll-op=“ack”>
Príkaz sa používa pre potvrdenie prijatia správy, ktorá je následne z fronty odstránená.

Príklad príkazu <poll-op=“ack”>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <poll op="ack" msgID="12345"/>
       <clTRID>ABC-12346</clTRID>
     </command>
</epp>
Príklad odpovede na tento <poll-op=“ack>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <response>
       <result code="1000">
         <msg>Command completed successfully</msg>
       </result>
       <msgQ count="4" id="12345"/>
       <trID>
         <clTRID>ABC-12346</clTRID>
         <svTRID>54322-XYZ</svTRID>
      </trID>
     </response>
</epp>
Príkaz <check>
Príkaz <check> je totožný s definíciou v RFC. Príkaz <check> sa používa na overenie dostupnosti jednotlivých objektov v systéme.

<check> pre Doménu
Príkaz <check> sa v tomto prípade používa na zistenie, či sa Doména nachádza v Registri, spravidla s cieľom zistiť, či je vybranú Doménu možné zaregistrovať.
Príkaz <check> musí v tomto prípade obsahovať jeden alebo viac prvkov <domain:name>, v ktorých sú uvedené plne kvalifikované názvy Domén na overenie (t.j. v tvare “názov.sk”).
Doména ako taká nemusí v systéme existovať, ale môže byť nedostupná napr. kvôli zablokovaniu príslušného reťazca alebo na základe súdneho príkazu.

Príklad príkazu <check> pre Doménu:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <check>
      <domain:check xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>test.sk</domain:name>
        <domain:name>next.sk</domain:name>
      </domain:check>
    </check>
    <clTRID>ABC-12345</clTRID>
  </command>
</epp>
Popis prvkov v odpovedi:

Prvok <domain:cd> obsahuje odpoveď, pričom pre každú Doménu sa uvádza samostatný prvok. Obsahuje nasledujúce podradené prvky:
Prvok <domain:name> s identifikáciou konkrétnej overovanej Domény. Tento prvok obsahuje atribút “avail” s hodnotou 1 (true) alebo 0 (false), kde 1 znamená, že Doména je voľná a je ju možné zaregistrovať (nenachádza sa v Registri) a 0 znamená, že Doména nie je dostupná na zaregistrovanie.
Prvok <domain:reason>, ktorý bližšie popisuje stav Domény. Tento prvok sa vytvára iba pri <domain:name> s hodnotou “avail” 0. Možné dôvody nedostupnosti Domény na registráciu sú napr.:
In use – Doména je už zaregistrovaná.
Blocked – názov Domény je blokovaný, napr. súdnym príkazom.
Príklad odpovede na tento <check>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <resData>
      <domain:chkData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:cd>
          <domain:name avail="1">next.sk</domain:name>
        </domain:cd>
        <domain:cd>
          <domain:name avail="0">test.sk</domain:name>
          <domain:reason>In use</domain:reason>
        </domain:cd>
      </domain:chkData>
    </resData>
    <trID>
      <clTRID>ABC-12345</clTRID>
      <svTRID>54322-XYZ</svTRID>
    </trID>
  </response>
</epp>
<check> pre Používateľa (kontakt)
Príkaz <check> sa v tomto prípade používa na zistenie, či je Používateľ (kontakt) zaevidovaný v Registri.
Musí obsahovať jeden alebo viac podradených prvkov <contact:id> s identifikátormi objektov Používateľ (kontakt), ktoré sa overujú.

Príklad príkazu <check> pre Používateľa (kontakt):
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <check>
      <contact:check xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>TEST-0001</contact:id>
        <contact:id>NEXT-0001</contact:id>
      </contact:check>
    </check>
    <clTRID>ABC-12345</clTRID>
  </command>
</epp>
Popis prvkov v odpovedi:

Prvok <contact:cd> obsahuje odpoveď, pričom pre každého Používateľa sa uvádza samostatný prvok. Obsahuje nasledujúce podradené prvky:
Prvok <contact:id> s ID konkrétneho overovaného Používateľa. Tento prvok obsahuje atribút “avail” s hodnotou 1 (true) alebo 0 (false), kde 1 znamená, že Používateľ v súčasnosti nie je zaevidovaný v Registri a 0 znamená, že Používateľ je v Registri evidovaný.
Prvok <contact:reason>, ktorý bližšie popisuje stav Používateľa. Tento prvok sa vytvára iba pri <contact:id> s hodnotou “avail” 0.
Príklad odpovede na tento <check>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <resData>
      <contact:chkData xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:cd>
          <contact:id avail="1">NEXT-0001</contact:id>
        </contact:cd>
        <contact:cd>
          <contact:id avail="0">TEST-0001</contact:id>
          <contact:reason>In use</contact:reason>
        </contact:cd>
      </contact:chkData>
    </resData>
    <trID>
      <clTRID>ABC-12345</clTRID>
      <svTRID>54322-XYZ</svTRID>
    </trID>
  </response>
</epp>
<check> pre menný server (host)
Prvok <host:name>, ktorý obsahuje mená menných serverov, ktoré majú byť dopytované.
Príklad príkazu <check> pre menný server (host):
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <check>
         <host:check
          xmlns:host="urn:ietf:params:xml:ns:host-1.0">
           <host:name>ns1.example.com</host:name>
           <host:name>ns2.example.com</host:name>
           <host:name>ns3.example.com</host:name>
         </host:check>
       </check>
       <clTRID>ABC-12345</clTRID>
     </command>
</epp>
Popis prvkov v odpovedi:

Prvok <host:cd> obsahuje odpoveď, pričom pre každý menný server (host) sa uvádza samostatný prvok. Obsahuje nasledujúce podradené prvky:
Prvok <host:name> s menom konkrétneho overovaného menného servera (host). Tento prvok obsahuje atribút “avail” s hodnotou 1 (true) alebo 0 (false), kde 1 znamená, že Host objekt v súčasnosti nie je zaevidovaný v Registri a 0 znamená, že menný server (host) je v Registri evidovaný a dostupný.
Prvok <contact:reason>, ktorý bližšie popisuje stav menného servera (host). Tento prvok sa vytvára iba pri <host:name> s hodnotou “avail” 0.
Príklad odpovede na tento <check>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <response>
       <result code="1000">
         <msg>Command completed successfully</msg>
       </result>
       <resData>
         <host:chkData
          xmlns:host="urn:ietf:params:xml:ns:host-1.0">
           <host:cd>
             <host:name avail="1">ns1.example.com</host:name>
           </host:cd>
           <host:cd>
             <host:name avail="0">ns2.example2.com</host:name>
             <host:reason>In use</host:reason>
           </host:cd>
           <host:cd>
             <host:name avail="1">ns3.example3.com</host:name>
           </host:cd>
         </host:chkData>
       </resData>
       <trID>
         <clTRID>ABC-12345</clTRID>
         <svTRID>54322-XYZ</svTRID>
       </trID>
     </response>
</epp>
Príkaz <create>
Príkaz <create> umožňuje vytvárať objekty v Registri.

<create> pre Doménu
Príkaz <create> umožňuje vytvoriť, t.j. zaregistrovať, novú Doménu. Príkaz <create> sa skladá z nasledovných podradených prvkov:

Prvku <domain:name> obsahujúceho korektný reťazec názvu Domény, ktorá má byť vytvorená.
Voliteľného prvku <domain:period>, ktorý určuje dĺžku registračného obdobia vybranej Domény. Možná dĺžka je 1 až 10 rokov. Pri vynechaní tohto prvku je prednastavená hodnota dĺžky registračného obdobia Domény 1 rok.
Prvku <domain:registrant>, ktorý identifikuje Používateľa, ktorý požiadal o registráciu Domény (t.j. budúceho Držiteľa).
Prvku <domain:contact>, ktorý identifikuje kontakt, ktorý má byť priradený k Doméne. Môže sa použiť viacnásobne.
Prvku <domain:authInfo>, v ktorom sa určuje autorizačné heslo pre vytváranú Doménu. Toto heslo sa môže vyžadovať pri niektorých ďalších akciách spojených s týmto objektom.
Voliteľného prvku <domain:ns>, ktorý obsahuje mená menných serverov.
Voliteľný <extension> prvok, ktorý obsahuje povinný <secDNS:create> podriadený prvok s ďalším voliteľmým <secDNS:maxSigLife> prvkom a povinných jeden alebo viac <secDNS:dsData> prvkov. Všetky štyri primárne podradené prvky z <secDNS: dsData> prvku – <secDNS:keyTag>, <secDNS:alg>, <secDNS:digestType> a <secDNS:digest> musia byť zadané.
Poznámka
Ak doména nebude podpísaná, rozšírenie DNSSEC musí byť vynechané. Schéma nepovoľuje prázdne hodnoty v prvkoch rozšírenia.

Poznámka
<secDNS:maxSigLife> hodnota je akceptovaná, ale nemá vplyv v prostredí SK-NICu.

Poznámka
Podradené prvky údajov kľúča<secDNS:keyData> v <secDNS:dsData> môžu byť zadané, ale keďže SK-NIC podporuje DS Data Interface, tieto údaje o kľúči budú síce zachované, ale ignorované.

Príklad príkazu <create>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <create>
         <domain:create
          xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
           <domain:name>example.com</domain:name>
           <domain:period unit="y">2</domain:period>
           <domain:ns>
             <domain:hostObj>ns1.example.net</domain:hostObj>
             <domain:hostObj>ns2.example.net</domain:hostObj>
           </domain:ns>
           <domain:registrant>jd1234</domain:registrant>
           <domain:contact type="admin">sh8013</domain:contact>
           <domain:contact type="tech">sh8013</domain:contact>
           <domain:authInfo>
             <domain:pw>2fooBAR</domain:pw>
           </domain:authInfo>
         </domain:create>
       </create>
       <clTRID>ABC-12345</clTRID>
     </command>
   </epp>
Rovnaký príkaz vrátane DNSSEC rozšírenia:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <create>
         <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
           <domain:name>example.com</domain:name>
           <domain:period unit="y">2</domain:period>
           <domain:ns>
             <domain:hostObj>ns1.example.net</domain:hostObj>
             <domain:hostObj>ns2.example.net</domain:hostObj>
           </domain:ns>
           <domain:registrant>jd1234</domain:registrant>
           <domain:contact type="admin">sh8013</domain:contact>
           <domain:contact type="tech">sh8013</domain:contact>
           <domain:authInfo>
             <domain:pw>2fooBAR</domain:pw>
           </domain:authInfo>
         </domain:create>
       </create>
       <extension>
         <secDNS:create xmlns:secDNS="urn:ietf:params:xml:ns:secDNS-1.1">
           <secDNS:maxSigLife>604800</secDNS:maxSigLife>
           <secDNS:dsData>
             <secDNS:keyTag>12345</secDNS:keyTag>
             <secDNS:alg>3</secDNS:alg>
             <secDNS:digestType>1</secDNS:digestType>
             <secDNS:digest>49FD46E6C4B45C55D4AC</secDNS:digest>
           </secDNS:dsData>
         </secDNS:create>
       </extension>
       <clTRID>ABC-12345</clTRID>
     </command>
   </epp>
Popis prvkov v odpovedi:

Prvok <domain:name> s názvom Domény pre spárovanie s odpoveďou.
Prvok <domain:crDate> obsahujúci potvrdzujúci dátum a čas zaregistrovania (vytvorenia) Domény.
Voliteľný prvok <domain:exDate>, ktorý obsahuje dátum a čas exspirácie Domény. Odpoveď systému SK-NIC obsahuje tento dátum vždy.
Príklad odpovede na tento <create>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <resData>
      <domain:creData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>test.sk</domain:name>
        <domain:crDate>1999-04-03T22:00:00.0Z</domain:crDate>
        <domain:exDate>2001-04-03T22:00:00.0Z</domain:exDate>
      </domain:creData>
    </resData>
    <trID>
      <clTRID>ABC-12345</clTRID>
      <svTRID>54321-XYZ</svTRID>
    </trID>
  </response>
</epp>
<create> pre Používateľa (kontakt)

Príkaz <create> umožňuje zaevidovať Používateľa (vytvoriť objekt kontakt). Príkaz <create> pozostáva z nasledujúcich podradených prvkov, ktoré identifikujú vytváraného Používateľa, a to:

Prvok <contact:id>, ktorý obsahuje identifikátor Používateľa.
Prvok <contact:postalInfo>, ktorý obsahuje slovnú identifikáciu Používateľa a informácie o adrese sídla, resp. trvalého bydliska Používateľa (podľa právnej formy). Prvok obsahuje nasledovné podradené prvky:
Prvok <contact: name>, v ktorom sa uvádza meno a priezvisko Používateľa. Pri právnickej osobe (konštanta “CORP”) sa zadá obchodný názov spoločnosti.
Voliteľný prvok <contact:org>, v ktorom sa uvádza názov spoločnosti, ktorú Používateľ reprezentuje.
Prvok <contact:addr>, ktorý obsahuje informácie o adrese Používateľa (pri fyzickej osobe sa uvádza adresa trvalého bydliska, pri právnickej osobe adresa sídla). Obsahuje nasledujúce podradené prvky:
Prvok <contact:street>, v ktorom sa uvádza názov ulice. Prvok môže byť použitý maximálne trikrát, a v prípade potreby je možné uviesť aj časť obce alebo ďalšie špecifiká adresy.
Prvok <contact:city>, v ktorom sa uvádza názov mesta.
Voliteľný prvok <contact:sp>, v ktorom sa uvádza názov regiónu, t.j. názov provincie, kraja, resp. nižšieho štátu v rámci federatívneho typu štátu, a to pre krajiny, kde je takéto členenie bežné. Pri slovenských adresách sa nepoužíva.
Prvok <contact:pc>, v ktorom sa uvádza poštové smerovacie číslo.
Prvok <contact:cc>, v ktorom sa uvádza kód krajiny (štandardne podľa ISO 3166-2).
Prvok <contact:voice>, v ktorom sa uvádza primárne platné telefónne číslo Používateľa. Telefónne číslo sa uvádza s predvoľbou krajiny, ktorá ja oddelená s bodkou.
Voliteľný prvok <contact:fax>, v ktorom sa uvádza faxové číslo Používateľa.
Prvok <contact:email>, v ktorom sa uvádza primárna e-mailová adresa Používateľa.
Prvok <contact:authInfo>, v ktorom sa určuje autorizačné heslo pre vytváraného Používateľa. Toto heslo sa môže vyžadovať pri niektorých ďalších akciách spojených s týmto objektom.
Voliteľný prvok <contact:disclose>, ktorý slúži na zverejňovanie určitých údajov, ktoré sa v preddefinovanom nastavení nezverejňujú. Pre príklady použitia pozrite sekciu Často kladené otázky.
Prvok <extension>, v ktorom sa uvádza právna forma Používateľa. Pri fyzickej osobe (konštanta “PERS”) sa udáva dátum narodenia a pri právnickej osobe a fyzickej osobe – podnikateľovi (konštanta “CORP”) sa udáva identifikačné číslo organizácie. Pre slovenské právnické osoby sa tu uvádza IČO, pre zahraničné právnické osoby ekvivalent z príslušného oficiálneho registra. Dátum narodenia sa pri fyzických osobách zadáva v tvare RRRR-MM-DD, napríklad 1987-01-01. Dátum narodenia nie je povinný údaj, ale pre presnejšiu identifikáciu Používateľa a najmä pre preukázanie nároku k Doméne odporúčame tento údaj vyplniť.
Poznámka
Formát dátumu sa bude v budúcnosti meniť na slovenský formát.

Príklad príkazu <create> pre Používateľa (kontakt):
<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <create>
      <contact:create xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>sh8013</contact:id>
        <contact:postalInfo type="int">
          <contact:name>John Doe</contact:name>
          <contact:org>Example Inc.</contact:org>
          <contact:addr>
            <contact:street>123 Example Dr.</contact:street>
            <contact:street>Suite 100</contact:street>
            <contact:city>Dulles</contact:city>
            <contact:sp>VA</contact:sp>
            <contact:pc>20166-6503</contact:pc>
            <contact:cc>US</contact:cc>
          </contact:addr>
        </contact:postalInfo>
        <contact:voice x="1234">+1.7035555555</contact:voice>
        <contact:fax>+1.7035555556</contact:fax>
        <contact:email>jdoe@example.com</contact:email>
        <contact:authInfo>
          <contact:pw>2fooBAR</contact:pw>
        </contact:authInfo>
        <contact:disclose flag="0">
          <contact:voice />
          <contact:email />
        </contact:disclose>
      </contact:create>
    </create>
    <extension>
      <skContactIdent:create xmlns:skContactIdent="http://www.sk-nic.sk/xml/epp/sk-contact-ident-0.2">
        <skContactIdent:legalForm>CORP</skContactIdent:legalForm>
        <skContactIdent:identValue>
          <skContactIdent:corpIdent>1234567890</skContactIdent:corpIdent>
        </skContactIdent:identValue>
      </skContactIdent:create>
    </extension>
    <clTRID>ABC-12345</clTRID>
  </command>
</epp>
Popis prvkov v odpovedi:

Prvok <contact:id>, ktorý obsahuje príslušný jedinečný identifikátor Používateľa.
Prvok <contact:crDate>, ktorý obsahuje potvrdzujúci dátum a čas, kedy bol Používateľ zaevidovaný (vytvorený) v Registri.
Príklad odpovede na tento <create>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <resData>
      <contact:creData xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>sh8013</contact:id>
        <contact:crDate>1999-04-03T22:00:00.0Z</contact:crDate>
      </contact:creData>
    </resData>
    <trID>
      <clTRID>ABC-12345</clTRID>
      <svTRID>54321-XYZ</svTRID>
    </trID>
  </response>
</epp>
<create> pre menný server (host)

Príkaz <create> umožňuje vytvoriť nový menný server (host). Príkaz <create> musí obsahovať tieto podradené prvky:

Prvok <host:name>, ktorý obsahuje meno menného servera (host), ktorý sa má vytvoriť.
Jeden a viac <host:addr>, ktoré obsahujú IP adresy pridružné k mennému serveru (host). Viac na RFC 5732 sekcia 3.2.1.
Príklad príkazu <create> pre menný server:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <create>
         <host:create
          xmlns:host="urn:ietf:params:xml:ns:host-1.0">
           <host:name>ns1.example.com</host:name>
           <host:addr ip="v4">192.0.2.2</host:addr>
           <host:addr ip="v4">192.0.2.29</host:addr>
           <host:addr ip="v6">1080:0:0:0:8:800:200C:417A</host:addr>
         </host:create>
       </create>
       <clTRID>ABC-12345</clTRID>
     </command>
</epp>
Príklad odpovede na tento <create>:
Popis prvkov v odpovedi:

Prvok <host:name>, ktorý obsahuje meno menného servera (host), ktorý bol vytvorený.
Prvok <host:crDate>, ktorý obsahuje dátum a čas, kedy bol menný server (host) vytvorený.
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <response>
       <result code="1000">
         <msg>Command completed successfully</msg>
       </result>
       <resData>
         <host:creData
          xmlns:host="urn:ietf:params:xml:ns:host-1.0">
           <host:name>ns1.example.com</host:name>
           <host:crDate>1999-04-03T22:00:00.0Z</host:crDate>
         </host:creData>
       </resData>
       <trID>
         <clTRID>ABC-12345</clTRID>
         <svTRID>54322-XYZ</svTRID>
       </trID>
     </response>
</epp>
Príkaz <delete>
Tento príkaz umožňuje vymazať Doménu, t.j. ukončiť jej registračné obdobie a vypovedať príslušnú Zmluvu o Doméne. Príkaz <delete> musí obsahovať podradený prvok <domain:name>, v ktorom sa identifikuje názov Domény, ktorá má byť vymazaná.

Doménu nie je možné vymazať vždy – za určitých okolností môže byť tento úkon zablokovaný, napr. na základe súdneho príkazu.

Príklad príkazu <delete> pre Doménu:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <delete>
      <domain:delete xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>test.sk</domain:name>
      </domain:delete>
    </delete>
    <clTRID>ABC-12345</clTRID>
  </command>
</epp>
Príklad odpovede na tento <delete>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
   <response>
      <result code="1000">
         <msg>Command completed successfully</msg>
      </result>
      <trID>
         <clTRID>ABC-12345</clTRID>
         <svTRID>54321-XYZ</svTRID>
      </trID>
   </response>
</epp>
<delete> pre Používateľa (kontakt)

Tento príkaz umožňuje vymazať Používateľa z Registra a ukončiť tak jeho evidenciu. Príkaz <delete> musí obsahovať podradený prvok <contact:ID> so správne prideleným identifikátorom Používateľa, ktorý má byť vymazaný.

Poznámka
Používateľ nemôže byť vymazaný, ak je prepojený s inými, resp. priradený k iným objektom!

Príklad príkazu <delete> pre Používateľa:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <delete>
      <contact:delete xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>TEST-0001</contact:id>
      </contact:delete>
    </delete>
    <clTRID>ABC-12345</clTRID>
  </command>
</epp>
Príklad odpovede na tento <delete>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
   <response>
      <result code="1000">
         <msg>Command completed successfully</msg>
      </result>
      <trID>
         <clTRID>ABC-12345</clTRID>
         <svTRID>54321-XYZ</svTRID>
      </trID>
   </response>
</epp>
<delete> pre menný server (host)

Tento príkaz umožňuje vymazať menný server (host) z Registra a ukončiť tak jeho evidenciu. Príkaz <delete> musí obsahovať podradený prvok <host:name>, ktorý obsahuje meno menného serveru (host), ktorý má byť vymazaný.

Poznámka
Menný server (host) nemôže byť vymazaný, ak je prepojený s inými, resp. priradený k iným objektom!

Príklad príkazu <delete> pre menný server (host):
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <delete>
         <host:delete
          xmlns:host="urn:ietf:params:xml:ns:host-1.0">
           <host:name>ns1.example.com</host:name>
         </host:delete>
       </delete>
       <clTRID>ABC-12345</clTRID>
     </command>
</epp>
Príklad odpovede na tento <delete>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <response>
       <result code="1000">
         <msg>Command completed successfully</msg>
       </result>
       <trID>
         <clTRID>ABC-12345</clTRID>
         <svTRID>54321-XYZ</svTRID>
       </trID>
     </response>
</epp>
Príkaz <info>
Príkaz <info> sa používa na zistenie podrobnejších informácií o existujúcom objekte. Odpovede na tento príkaz sa môžu líšiť v závislosti od oprávnenosti klienta systému.

<info> pre Doménu
Príkaz <info> musí v tomto prípade obsahovať podradený prvok <domain:name> s názvom Domény, o ktorej sa zisťujú informácie.
Voliteľný prvok je <domain:authInfo>, ktorý obsahuje autorizačné heslo k Doméne.

Príklad príkazu <info> pre Doménu:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <info>
      <domain:info xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>test.sk</domain:name>
      </domain:info>
    </info>
    <clTRID>ABC-12345</clTRID>
  </command>
</epp>
Popis prvkov v odpovedi:

Prvok <domain:name>, ktorý obsahuje príslušný názov Domény.
Prvok <domain:roid>, ktorý obsahuje identifikátor úložiska priradený Doméne pri vytvorení jej objektu.
Voliteľný prvok <domain:status>, ktorý obsahuje súčasný popis stavu Domény.
Voliteľný prvok <domain:ns>, ktorý obsahuje meno delegovaných menných serverov (host), prípadne ich atribútov pridružených k doméne. Viac informácií na RFC 5731 sekcia 1.1.
Voliteľný podradený prvok <domain:host>, ktorý obsahuje meno podradeného menného servera (host).
Prvok <domain:clID>, ktorý obsahuje identifikátor aktuálneho Autorizovaného registrátora Domény.
Voliteľný prvok <domain:crID>, ktorý obsahuje identifikátor Registrátora, ktorý pôvodne zaregistroval (vytvoril) Doménu.
Voliteľný prvok <domain:crDate>, ktorý obsahuje dátum a čas, kedy bola Doména v súčasnom registračnom období zaregistrovaná (vytvorená).
Voliteľný prvok <domain:upID>, ktorý obsahuje identifikátor Registrátora, ktorý naposledy aktualizoval údaje o Doméne. Tento prvok sa neposkytuje, ak Doména nebola nikdy aktualizovaná.
Voliteľný prvok <domain:upDate>, ktorý obsahuje dátum a čas, kedy bola Doména naposledy aktualizovaná. Tento prvok sa neposkytuje, ak Doména nebola nikdy aktualizovaná.
Voliteľný prvok <domain:exDate>, ktorý obsahuje dátum a čas exspirácie Domény.
Voliteľný prvok <domain:trDate>, ktorý obsahuje dátum a čas poslednej úspešnej zmeny Autorizovaného registrátora Domény.
Voliteľný prvok <domain:authInfo>, ktorý obsahuje informáciu, či je Doména chránená heslom.
Voliteľný <secDNS:infData> podriadený prvok obsiahnutý pod <extension>, ak je doména chránená DNSSECom, môže obsahovať ďalšie prvky
voliteľný <secDNS:maxSigLife> podradený
a jeden alebo viac <secDNS:dsData>.
Poznámka
Voliteľný prvok pri odpovedi znamená, že bude poskytnutý v prípade, ak má daný objekt tento prvok vyplnený nejakou hodnotou. Prázdne, t.j. nevyplnené hodnoty sa neuvádzajú. Nižšie uvedený príklad obsahuje aj odpoveď na DNSSEC.

Príklad odpovede na tento <info>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <resData>
      <domain:infData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
           <domain:name>example.com</domain:name>
           <domain:roid>EXAMPLE1-REP</domain:roid>
           <domain:status s="ok"/>
           <domain:registrant>jd1234</domain:registrant>
           <domain:contact type="admin">sh8013</domain:contact>
           <domain:contact type="tech">sh8013</domain:contact>
           <domain:ns>
             <domain:hostObj>ns1.example.com</domain:hostObj>
             <domain:hostObj>ns1.example.net</domain:hostObj>
           </domain:ns>
           <domain:host>ns1.example.com</domain:host>
           <domain:host>ns2.example.com</domain:host>
           <domain:clID>ClientX</domain:clID>
           <domain:crID>ClientY</domain:crID>
          <domain:crDate>1999-04-03T22:00:00.0Z</domain:crDate>
           <domain:upID>ClientX</domain:upID>
           <domain:upDate>1999-12-03T09:00:00.0Z</domain:upDate>
           <domain:exDate>2005-04-03T22:00:00.0Z</domain:exDate>
           <domain:trDate>2000-04-08T09:00:00.0Z</domain:trDate>
           <domain:authInfo>
             <domain:pw>2fooBAR</domain:pw>
           </domain:authInfo>
         </domain:infData>
    </resData>
    <extension>
         <secDNS:infData xmlns:secDNS="urn:ietf:params:xml:ns:secDNS-1.1">
           <secDNS:dsData>
             <secDNS:keyTag>12345</secDNS:keyTag>
             <secDNS:alg>3</secDNS:alg>
             <secDNS:digestType>1</secDNS:digestType>
             <secDNS:digest>49FD46E6C4B45C55D4AC</secDNS:digest>
           </secDNS:dsData>
         </secDNS:infData>
    </extension>
    <trID>
      <clTRID>ABC-12345</clTRID>
      <svTRID>54322-XYZ</svTRID>
    </trID>
  </response>
</epp>
<info> pre Používateľa (kontakt)

Príkaz <info> musí v tom prípade obsahovať podradený prvok <contact:info> a ten zase podradené prvky:

Prvok <contact:ID> obsahujúci identifikátor Používateľa, o ktorom sa zisťujú informácie.
Voliteľný prvok <contact:authInfo>, ktorý obsahuje autorizačné heslo k Používateľovi.
Príklad príkazu <info> pre Používateľa:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <info>
         <contact:info
          xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
           <contact:id>sh8013</contact:id>
           <contact:authInfo>
             <contact:pw>2fooBAR</contact:pw>
           </contact:authInfo>
         </contact:info>
       </info>
       <clTRID>ABC-12345</clTRID>
     </command>
</epp>
Popis prvkov v odpovedi:

Prvok <contact:id>, ktorý obsahuje príslušný identifikátor Používateľa.
Prvok <contact:roid>, ktorý obsahuje identifikátor úložiska priradený k Používateľovi pri jeho vytvorení.
Prvok <contact:status>, ktorý podrobnejšie popisuje stav Používateľa. Tento prvok v súčasnej verzii nepodporujeme.
Prvok <contact:postalInfo>, ktorý obsahuje informácie o adrese Používateľa. Obsahuje nasledujúce podradené prvky:
Prvok <contact:name>, v ktorom sa uvádza meno a priezvisko Používateľa. Pri právnickej osobe (konštanta “CORP”) to môže byť aj obchodný názov spoločnosti alebo meno osoby, ktorá zastupuje danú spoločnosť.
Voliteľný prvok <contact:org>, v ktorom sa uvádza názov spoločnosti, ktorú Používateľ reprezentuje, vypĺňa sa, iba ak sa jedná o právnickú osobu, pri fyzickej osobe sa tento prvok neposkytuje.
Prvok <contact:addr>, ktorý obsahuje informácie o adrese kontaktu. Prvok obsahuje nasledujúce podradené prvky:
Prvok <contact:street>, ktorý obsahuje názov ulice. Prvok môže byť použitý trikrát.
Prvok <contact:city>, ktorý obsahuje názov mesta.
Voliteľný prvok <contact:sp>, ktorý obsahuje názov regiónu (štátu federatívnej krajiny, provincie a podobne).
Prvok <contact:pc>, ktorý obsahuje poštové smerovacie číslo.
Prvok <contact:cc>, ktorý obsahuje kód krajiny.
Prvok <contact:voice>, ktorý obsahuje primárne telefónne číslo Používateľa. Telefónne číslo sa uvádza s predvoľbou krajiny, ktorá ja oddelená s bodkou.
Voliteľný prvok <contact:fax>, ktorý obsahuje faxové číslo Používateľa.
Prvok <contact:email>, ktorý obsahuje primárnu e-mailovú adresu Používateľa.
Prvok <contact:clid>, ktorý obsahuje identifikátor aktuálneho Autorizovaného registrátora kontaktných údajov.
Prvok <contact:crID>, ktorý obsahuje identifikátor Registrátora, ktorý Používateľa zaevidoval (vytvoril).
Prvok <contact:crDate>, ktorý obsahuje dátum a čas, kedy bol Používateľ zaevidovaný.
Voliteľný prvok <contact:upID>, ktorý obsahuje identifikátor Registrátora, ktorý naposledy zmenil údaje Používateľa.
Voliteľný prvok <contact:upDate>, ktorý obsahuje dátum a čas poslednej zmeny údajov Používateľa.
Voliteľný prvok <contact:trDate>, ktorý obsahuje dátum a čas poslednej úspešnej zmeny Autorizovaného registrátora kontaktných údajov.
Voliteľný prvok <contact:authinfo>, ktorý obsahuje informáciu, či je Používateľ chránený heslom.
Voliteľný prvok <contact:disclose>, obsahuje podradené prvky, ktoré sa zobrazujú tretím stranám. Pre použitie pozrite sekciu Často kladené otázky.
Príklad odpovede na toto <info>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <resData>
      <contact:infData xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>sh8013</contact:id>
        <contact:roid>SH8013-REP</contact:roid>
        <contact:ident legalForm="PO">1234567890</contact:ident>
        <contact:status s="linked"/>
        <contact:status s="clientDeleteProhibited"/>
        <contact:postalInfo>
          <contact:name>John Doe</contact:name>
          <contact:org>Example Inc.</contact:org>
          <contact:addr>
            <contact:street>123 Example Dr.</contact:street>
            <contact:street>Suite 100</contact:street>
            <contact:city>Dulles</contact:city>
            <contact:sp>VA</contact:sp>
            <contact:pc>20166-6503</contact:pc>
            <contact:cc>US</contact:cc>
          </contact:addr>
        </contact:postalInfo>
        <contact:voice>+421.7035555555</contact:voice>
        <contact:fax>+421.7035555556</contact:fax>
        <contact:email>jdoe@example.com</contact:email>
        <contact:clID>ClientY</contact:clID>
        <contact:crID>ClientX</contact:crID>
        <contact:crDate>1999-04-03T22:00:00.0Z</contact:crDate>
        <contact:upID>ClientX</contact:upID>
        <contact:upDate>1999-12-03T09:00:00.0Z</contact:upDate>
        <contact:trDate>2000-04-08T09:00:00.0Z</contact:trDate>
        <contact:authInfo>2fooBAR</contact:authInfo>
        <contact:disclose flag="0">
          <contact:voice/>
          <contact:email/>
        </contact:disclose>
      </contact:infData>
    </resData>
    <trID>
      <clTRID>ABC-12345</clTRID>
      <svTRID>54322-XYZ</svTRID>
    </trID>
  </response>
</epp>
<info> pre menný server (host)

Príkaz <info> musí v tom prípade obsahovať <host:info> a nasledujúci podradený prvok <host:name>, ktorý obsahuje meno dopytovaného menného servera (host), o ktorom chceme zistiť informácie.

Príklad príkazu <info> pre menný server (host):
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <info>
         <host:info
          xmlns:host="urn:ietf:params:xml:ns:host-1.0">
           <host:name>ns1.example.com</host:name>
         </host:info>
       </info>
       <clTRID>ABC-12345</clTRID>
     </command>
</epp>
Popis prvkov v odpovedi:

Prvok <host:name>, ktorý obsahuje meno dopytovaného menného servera (host).
Prvok <host:roid>, ktorý obsahuje identifikátor úložiska priradený k mennému serveru (host) pri jeho vytvorení.
Prvok <host:status>, ktorý obsahuje stav, v ktorom sa menný server (host) nachádza.
Prvok <host:addr>, ktorý obsahuje IP adresy menného servera (host).
Prvok <host:clID>, ktorý obsahuje ID súčasného Registrátora menného servera (host) objektu.
Prvok <host:crID>, ktorý obsahuje ID Registrátora, ktorý objekt vytvoril.
Prvok <host:crDate>, ktorý obsahuje dátum a čas, kedy bol menný server (host) vytvorený.
Voliteľný prvok <host:upID>, ktorý obsahuje ID Registrátora, ktorý naposledy upravoval menný server (host).
Voliteľný prvok <host:upDate>, ktorý obsahuje posledný dátum a čas úpravy menného servera (host).
Voliteľný prvok <host:trDate>,ktorý obsahuje dátum čas transferu menného servera (host).
Príklad odpovede pre toto <info>:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <response>
       <result code="1000">
         <msg>Command completed successfully</msg>
       </result>
       <resData>
         <host:infData
          xmlns:host="urn:ietf:params:xml:ns:host-1.0">
           <host:name>ns1.example.com</host:name>
           <host:roid>NS1_EXAMPLE1-REP</host:roid>
           <host:status s="linked"/>
           <host:status s="clientUpdateProhibited"/>
           <host:addr ip="v4">192.0.2.2</host:addr>
           <host:addr ip="v4">192.0.2.29</host:addr>
           <host:addr ip="v6">1080:0:0:0:8:800:200C:417A</host:addr>
           <host:clID>ClientY</host:clID>
           <host:crID>ClientX</host:crID>
           <host:crDate>1999-04-03T22:00:00.0Z</host:crDate>
           <host:upID>ClientX</host:upID>
           <host:upDate>1999-12-03T09:00:00.0Z</host:upDate>
           <host:trDate>2000-04-08T09:00:00.0Z</host:trDate>
         </host:infData>
       </resData>
       <trID>
         <clTRID>ABC-12345</clTRID>
         <svTRID>54322-XYZ</svTRID>
       </trID>
     </response>
</epp>
Príkaz <transfer>
Príkaz <transfer> umožňuje zaslanie žiadosti o zmenu Autorizovaného registrátora (prevod) objektu. V súčasnej verzii systému je možné previesť iba objekt Doména.

Poznámka
Každý EPP príkaz <transfer> musí obsahovať “op” atribút, ktorý identifikuje transfer operácie, ktorý má byť vykonaný.

Zoznam podporovaných operácií:
<transfer op=“request”>
<transfer op=“cancel”>
<transfer op=“approve”>
<transfer op=“reject”>
Pri tejto operácii je vybranej doméne zmenený Autorizovaný registrátor domény. V tejto požiadavke musí byť správne uvedené autorizačné heslo domény, doména nemôže mať stav clientTransferProhibited! alebo serverTransferProhibited.

Transfer domény je vykonaný okamžite.

<transfer op=“cancel”> (Zrušenie žiadosti)
Doména, ktorá má pri transfere stále stav “pending”, môže byť Registrátorom, ktorý zadal požiadavku o transfer, zrušená.

<transfer op=“approve”> (Schválenie žiadosti)
Pôvodný Registrátor domény môže podľa vlastného úváženia schváliť žiadosť o transfer Domény na nového Registrátora ešte pred dátumom transferu.

<transfer op=“reject”> (Zamietnutie žiadosti)
Pôvodný Registrátor domény môže zamietnuť žiadosť o transfer domény. V princípe operácia nie je poskytnutá.

<transfer> pre Doménu

Príkaz <transfer> musí v tomto prípade obsahovať prvok <domain:transfer> s nasledujúcimi podradenými prvkami:

Prvok <domain:name> s názvom Domény, ktorej Autorizovaný registrátor má byť zmenený.
Voliteľný prvok <domain:period>, ktorý určuje dĺžku registračného obdobia vybranej Domény. Možná dĺžka je 1 až 10 rokov.
Prvok <domain:authInfo>, v ktorom musí byť uvedené správne heslo Domény.
Poznámka
Po zmene registrátora si nezabudnite zmeniť kontakty na Doméne, inak nebudete môcť vykonávať niektoré akcie nad Doménou.

Príklad príkazu <transfer op=“request> pre Doménu:
<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <transfer op="request">
      <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>test.sk</domain:name>
        <domain:period unit="y">1</domain:period>
        <domain:authInfo>
          <domain:pw roid="JD1234-REP">2fooBAR</domain:pw>
        </domain:authInfo>
      </domain:transfer>
    </transfer>
    <clTRID>ABC-12345</clTRID>
  </command>
</epp>
Príklad odpovede pre tento <transfer>:
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1001">
      <msg>Command completed successfully; action pending</msg>
    </result>
    <trID>
      <clTRID>ABC-12345</clTRID>
      <svTRID>54322-XYZ</svTRID>
    </trID>
  </response>
</epp>
Príkaz <update>
<update> pre Doménu

Príkaz <update> umožňuje klientovi zmeniť, resp. aktualizovať údaje objektu, v tomto prípade Domény. Príkaz <update> musí v tomto prípade obsahovať prvok <domain:update> a v ňom nasledovné podradené prvky:

Prvok <domain:name> obsahujúci názov Domény, ktorej údaje majú byť zmenené.
Voliteľný prvok <domain:add> obsahujúci údaje, ktoré majú byť doplnené k Doméne:
Voliteľný prvok <domain:ns>, ktorý obsahuje meno delegovaných menných serverov (hosts), prípadne jeho atribútov pridružených k doménam. Viac informácií na RFC 5731 sekcia 1.1.
Prvok <domain:contact>, ktorý identifikuje kontakt na priradenie. Môže byť použitý viacnásobne.
Prvok <domain:status> obsahujúci stav, ktorý má byť priradený k Doméne.
Voliteľný prvok <domain:rem> obsahujúci údaje, ktoré majú byť z Domény odstránené:
Voliteľný prvok <domain:ns>, ktorý obsahuje meno delegovaných menných serverov (hosts), prípadne jeho atribútov pridružených k doménam. Viac informácií na RFC 5731 sekcia 1.1.
Prvok <domain:contact>, ktorý identifikuje kontakt, ktorý sa má odstrániť. Môže byť použitý viacnásobne.
Prvok <domain:status> obsahujúci stav, ktorý má byť odstránený z Domény.
Voliteľný prvok <domain:chg> obsahujúci podradené prvky s hodnotami, ktoré majú v danej Doméne zmenené:
Prvok <domain:registrant>, ktorý obsahuje identifikátor nového Držiteľa Domény. Týmto sa vykoná prevod Držiteľa na nového Držiteľa.
Prvok <domain:authInfo> obsahujúci autorizačné informácie (heslo) spojené s Doménou, ktorým sa nahradí pôvodné heslo.
Voliteľný <extension> prvok, ktorý obsahuje
Voliteľný <secDNS:update> prvok obsahujúci ďalej
Voliteľný <secDNS:rem> prvok, ktorý obsahuje
– buď <secDNS:dsData> prvok na odstránenie konkrétneho DS záznamu pomocou všetkých štyroch prvkov – <secDNS:keyTag>, <secDNS:alg>, <secDNS:digestType> a <secDNS:digest>.
– alebo voliteľný <secDNS:all> prvok na odstránenie všetkých DS a kľúčov, ak obsahuje pravdivostnú hodnotu true. Pravdivostná hodnota false neurobí nič.
Voliteľný <secDNS:add> prvok na pridanie ďalších DNSSEC informácií do existujúceho záznamu, ktorý obsahuje aspoň jeden <secDNS:dsData> podradený prvok so všetkými štyrmi pomocnými prvkami <secDNS:keyTag>, <secDNS:alg>, <secDNS:digestType > a <secDNS:digest>.
Voliteľný <secDNS:chg> prvok na zmenu existujúcich informácií DNSSEC, ktorý obsahuje voliteľný <secDNS:maxSigLife> prvok, ktorý oznamuje preferenciu podradenej zóny o počte sekúnd po generovaní podpisu, keď platnosť podpisu nadradenej zóny na informáciách DS poskytnutých podradenou zónou vyprší. V prostredí SK-NICu je možné tento prvok zmeniť, ale nemá žiadny vplyv.
Poznámka
Ak doména nie je podpísaná, musí byť vynechané rozšírenie DNSSEC. Schéma nepovoľuje prázdne hodnoty v prvkoch rozšírenia.

Poznámka
Schéma XML zakazuje miešanie prvkov <secDNS:all/> a <secDNS:dsData>.
Odstránenie všetkých DS informácií prostredníctvom <secDNS:rem> a <secDNS:all> môže odstrániť schopnosť nadradenej zóny zabezpečiť delegovanie do podradenej zóny.

Poznámka
Podradené prvky údajov kľúča<secDNS:keyData> v <secDNS:dsData> môžu byť zadané, ale keďže SK-NIC podporuje DS Data Interface, tieto údaje o kľúči budú síce zachované, ale ignorované.

Poznámka
Špecifické nastavenia ako napríklad „clientUpdateProhibited“ môžu byť na doménu pridané iba pomocou príkazu <update>.

Príkaz <update> je možné použiť aj na nastavenie konkrétnych príznakov popísaných v časti Základné informácie EPP – Pridanie a odobratie osobitných príznakov. Nasledujúci príklad obsahuje aj dobrovoľné rozšírenie DNSSEC.

Príklad príkazu <update> pre doménu:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <update>
      <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>test.sk</domain:name>
        <domain:add>
             <domain:ns>
              <domain:hostObj>ns2.example.com</domain:hostObj>
             </domain:ns>
             <domain:contact type="tech">mak21</domain:contact>
             <domain:status s="clientHold"
              lang="en">Payment overdue.</domain:status>
           </domain:add>
           <domain:rem>
             <domain:ns>
               <domain:hostObj>ns1.example.com</domain:hostObj>
             </domain:ns>
             <domain:contact type="tech">sh8013</domain:contact>
             <domain:status s="clientUpdateProhibited"/>
           </domain:rem>
           <domain:chg>
             <domain:registrant>sh8013</domain:registrant>
             <domain:authInfo>
               <domain:pw>2BARfoo</domain:pw>
             </domain:authInfo>
           </domain:chg>
      </domain:update>
    </update>
    <extension>
         <secDNS:update xmlns:secDNS="urn:ietf:params:xml:ns:secDNS-1.1">
           <secDNS:rem>
             <secDNS:dsData>
               <secDNS:keyTag>12345</secDNS:keyTag>
               <secDNS:alg>3</secDNS:alg>
               <secDNS:digestType>1</secDNS:digestType>
               <secDNS:digest>38EC35D5B3A34B33C9B</secDNS:digest>
             </secDNS:dsData>
           </secDNS:rem>
           <secDNS:add>
             <secDNS:dsData>
               <secDNS:keyTag>12346</secDNS:keyTag>
               <secDNS:alg>3</secDNS:alg>
               <secDNS:digestType>1</secDNS:digestType>
               <secDNS:digest>38EC35D5B3A34B44C39B</secDNS:digest>
             </secDNS:dsData>
           </secDNS:add>
           <secDNS:chg>
             <secDNS:maxSigLife>605900</secDNS:maxSigLife>
           </secDNS:chg>
         </secDNS:update>
       </extension>
    <clTRID>ABC-12345</clTRID>
  </command>
</epp>
Príklad odpovede na tento <update>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
   <response>
      <result code="1000">
         <msg>Command completed successfully</msg>
      </result>
      <trID>
         <clTRID>ABC-12345</clTRID>
         <svTRID>54321-XYZ</svTRID>
      </trID>
   </response>
</epp>
<update> pre Používateľa (kontakt)

Príkaz musí v tomto prípade obsahovať prvok <contact:update> s nasledovnými podradenými prvkami:

Prvok <contact:id> obsahujúci príslušný Identifikátor Používateľa, ktorého údaje majú byť zmenené.
Prvok <contact:add> obsahujúci údaje, ktoré majú byť doplnené k Používateľovi:
Prvok <contact:status> obsahujúci stav, ktorý má byť priradený k Používateľovi. Tento prvok v súčasnej verzii nepodporujeme.
Prvok <contact:rem> obsahujúci údaje, ktoré majú byť pri Používateľovi odstránené:
Prvok <contact:status>, ktorý obsahuje stav na odstránenie. Tento prvok v súčasnej verzii nepodporujeme.
Prvok <contact:chg> obsahujúci podradené prvky s hodnotami, ktoré majú byť pri danom Používateľovi nahradené novými hodnotami:
Prvok <contact:postalInfo>, ktorý obsahujú informácie o adrese Používateľa, pričom tento prvok obsahuje podradené prvky:
Prvok <contact:name> s novým menom Používateľa.
Voliteľný prvok <contact:org> s novým názvom právnickej osoby, pod ktorú Používateľ patrí. Pri fyzickej osobe sa tento prvok nezadáva
Prvok <contact:addr>, ktorý obsahuje informácie o adrese kontaktu. Prvok obsahuje nasledujúce ďalšiu úroveň podradených prvkov:
Prvok <contact:street> s novým názvom ulice.
Prvok <contact:city> s novým názvom mesta.
Voliteľný prvok <contact:sp> s novým názvom regiónu (napr. štátom pri federatívnej krajiny alebo názvom provincie).
Prvok <contact:pc> s novým poštovým smerovacím číslom.
Prvok <contact:cc> s novým kódom krajiny.
Prvok <contact:voice> s novým primárnym telefónnym číslom Používateľa. Telefónne číslo sa uvádza s predvoľbou krajiny, ktorá ja oddelená s bodkou.
Voliteľný prvok <contact:fax> s novým faxovým číslom Používateľa.
Voliteľný prvok <contact:email> s novou primárnou e-mailovou adresou Používateľa.
Voliteľný prvok <contact:authInfo> s novým autorizačným heslom pre Používateľa.
Voliteľný prvok <contact:disclose> s novými údajmi, ktoré sa majú zverejňovať tretím stranám.
Príklad príkazu <update> pre Používateľa:
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <update>
         <contact:update
          xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
           <contact:id>sh8013</contact:id>
           <contact:add>
             <contact:status s="clientDeleteProhibited"/>
           </contact:add>
           <contact:chg>
             <contact:postalInfo type="int">
               <contact:org/>
               <contact:addr>
                 <contact:street>124 Example Dr.</contact:street>
                 <contact:street>Suite 200</contact:street>
                 <contact:city>Dulles</contact:city>
                 <contact:sp>VA</contact:sp>
                 <contact:pc>20166-6503</contact:pc>
                 <contact:cc>US</contact:cc>
               </contact:addr>
             </contact:postalInfo>
             <contact:voice>+1.7034444444</contact:voice>
             <contact:fax/>
             <contact:authInfo>
               <contact:pw>2fooBAR</contact:pw>
             </contact:authInfo>
             <contact:disclose flag="1">
               <contact:voice/>
               <contact:email/>
             </contact:disclose>
           </contact:chg>
         </contact:update>
       </update>
       <clTRID>ABC-12345</clTRID>
     </command>
   </epp>
Príklad odpovede na tento <update>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
   <response>
      <result code="1000">
         <msg>Command completed successfully</msg>
      </result>
      <trID>
         <clTRID>ABC-12345</clTRID>
         <svTRID>54321-XYZ</svTRID>
      </trID>
   </response>
</epp>
<update> pre menný server (host)

Príkaz musí v tomto prípade obsahovať prvok <host:update> s nasledovnými podradenými prvkami:

Prvok <host:name> obsahujúci meno menného servera (host), ktorého údaje majú byť zmenené.
Prvok <host:add> obsahujúci údaje, ktoré majú byť doplnené k mennému serveru (host):
Prvok <host:status> obsahujúci stav, ktorý má byť priradený k mennému serveru (host).
Prvok <host:addr>, ktorý obsahuje jeden alebo viac IP adries, ktoré majú pridané k mennému serveru (host).
Prvok <host:rem> obsahujúci údaje, ktoré majú byť pri mennom serveri (host) odstránené:
Prvok <host:status> obsahujúci stav, ktorý má byť odstránený z menného servera (host).
Prvok <host:addr>, ktorý obsahuje jednu alebo viac IP adries, ktoré majú byť odstránené z menného servera (host).
Prvok <host:chg> obsahujúci podradené prvky s hodnotami, ktoré majú byť pri danom mennom serveri (host) nahradené novými hodnotami:
Prvok <host:name>, ktorý obsahuje nové meno menného servera (host), ktorý by mal nahradiť existujúci pre daný názov servera.
Príklad príkazu <update> pre menný server (host):
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
     <command>
       <update>
         <host:update
          xmlns:host="urn:ietf:params:xml:ns:host-1.0">
           <host:name>ns1.example.com</host:name>
           <host:add>
             <host:addr ip="v4">192.0.2.22</host:addr>
             <host:status s="clientUpdateProhibited"/>
           </host:add>
           <host:rem>
             <host:addr ip="v6">1080:0:0:0:8:800:200417A</host:addr>
           </host:rem>
           <host:chg>
             <host:name>ns2.example.com</host:name>
           </host:chg>
         </host:update>
       </update>
       <clTRID>ABC-12345</clTRID>
     </command>
</epp>
Príkaz <renew>
<renew> pre Doménu

Príkaz <renew> umožňuje predĺženie registračného obdobia Domény. Príkaz <renew> musí obsahovať podradený prvok <domain:renew> a ten podradené prvky:

Prvok <domain:name> s názvom Domény, ktorej registračné obdobie má byť predĺžené.
Prvok <domain:curExpDate> s dátumom, ku ktorému končí platnosť súčasného registračného obdobia. Táto hodnota zabezpečuje, že opakované príkazy <renew> nevyústia do viacnásobných nepredpokladaných úspešných obnovení.
Voliteľný prvok <domain:period>, ktorý obsahuje dĺžku obdobia, o ktoré má byť registračné obdobie Domény predĺžené. Možnosť predĺženia je 1-10 rokov. Ak sa tento prvok nevyplní, preddefinovaná hodnota predĺženia bude 1 rok.
Príklad príkazu <renew>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <renew>
      <domain:renew xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>test.sk</domain:name>
        <domain:curExpDate>2000-04-03</domain:curExpDate>
        <domain:period unit="y">5</domain:period>
      </domain:renew>
    </renew>
    <clTRID>ABC-12345</clTRID>
  </command>
</epp>
Príklad odpovede na <renew>:
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <resData>
      <domain:renData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>test.sk</domain:name>
        <domain:exDate>2005-04-03T22:00:00.0Z</domain:exDate>
      </domain:renData>
    </resData>
    <trID>
      <clTRID>ABC-12345</clTRID>
      <svTRID>54322-XYZ</svTRID>
    </trID>
  </response>
</epp>

EPP systém SK-NIC podporuje niekoľko rozšírení. Ich zoznam je uvedený nižšie.

Príkaz pre zistenie informácií o Doméne
Príkaz pre Obnovenie Domény
Príkaz pre DNSSEC
Príkaz pre identifikáciu osoby
Doplňujúce kontaktné informácie

Príkaz pre zistenie informácií o Doméne
Ak má Doména stav „Vymazávaná: Ochranné obdobie“, EPP kód odpovede na príkaz <info> je rozšírený o špeciálny popis tohto stavu.

Príklad odpovede je uvedený nižšie.

<?xml version="1.0" encoding="utf-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
   <response>
      <result code="1000">
         <msg>Command completed successfully</msg>
      </result>
      <resData>
         <domain:infData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
            <domain:name>example.sk</domain:name>
         </domain:infData>
      </resData>
      <extension>
         <rgp:infData xmlns:rgp="urn:ietf:params:xml:ns:rgp-1.0">
            <rgp:rgpStatus s="redemptionPeriod" />
         </rgp:infData>
      </extension>
      <trID>
         <clTRID>ABC-12345</clTRID>
         <svTRID>54322-XYZ</svTRID>
      </trID>
   </response>
</epp>
Príkaz pre Obnovenie Domény
Ak je Doména v stave „Vymazávaná: Ochranné obdobie“, okrem bežného predĺženia registračného obdobia <renew> je ju možné aj obnoviť s použitím rozšíreného príkazu <update>.

Nižšie je uvedený príklad.

<?xml version="1.0" encoding="utf-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
   <command>
      <update>
         <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
            <domain:name>example.sk</domain:name>
            <domain:chg />
         </domain:update>
      </update>
      <extension>
         <rgp:update xmlns:rgp="urn:ietf:params:xml:ns:rgp-1.0">
            <rgp:restore op="request" />
         </rgp:update>
      </extension>
      <clTRID>ABC-12345</clTRID>
   </command>
</epp>
SK-NIC v súčasnosti nevyžaduje od registrátorov, aby zasielali „správu o obnovení“ ako súčasť obnovenia.

Príkaz pre DNSSEC
Rozšírenie na DNSSEC je podporované podľa RFC 5910 a RFC 4034.

Toto rozšírenie pridáva do mapovania názvov domén EPP ďalšie prvky.

Delegation Signer (DS) informácie sú publikované serverom DNS na označenie, že podradená zóna je digitálne podpísaná a že nadradená zóna rozpozná uvedený kľúč ako platný kľúč zóny pre podradenú zónu.

DS resource record (RR) obsahuje štyri polia: pole key tag (značka kľúča), číslo kľúčového algoritmu oktet, oktet identifikujúci algoritmus digestu a pole digest.

Informácie verejného kľúča poskytnuté klientom sa mapujú do formátov prezentačných polí DNSKEY RR opísaných v RFC 4034 v časti 2.2. DNSKEY RR obsahuje štyri polia: príznaky, oktet protokolu, oktet algoritmu a verejný kľúč.

Maximálna životnosť podpisu (maxSigLife) je voľba OPTIONAL podradenej pre počet sekúnd po generovaní podpisu, keď podpis nadradenej na informáciách DS poskytnutých podradenou exspiruje. Hodnota maxSigLife sa vzťahuje na záznam o prostriedkoch RRSIG (RR) cez DS RRset.

Server SK-NIC podporuje rozhranie DS data interface.

Poznámka
Jednotlivé použitia v rámci príkazov EPP sú popísané pod danými príkazmi.

<extension>
   <secDNS:create xmlns:secDNS="urn:ietf:params:xml:ns:secDNS-1.1">
      <secDNS:maxSigLife>604800</secDNS:maxSigLife>
      <secDNS:dsData>
         <secDNS:keyTag>12345</secDNS:keyTag>
         <secDNS:alg>3</secDNS:alg>
         <secDNS:digestType>1</secDNS:digestType>
         <secDNS:digest>49FD46E6C4B45C55D4AC</secDNS:digest>
      </secDNS:dsData>
   </secDNS:create>
</extension>
Príkaz pre identifikáciu osoby
Toto rozšírenie sa používa na rozlíšenie právnej formy Používateľa, a to najmä z dôvodu ochrany osobných údajov.
Pri fyzickej osobe (konštanta “PERS”) sa udáva dátum narodenia a pri právnickej osobe a fyzickej osobe – podnikateľovi (konštanta “CORP”) sa udáva identifikačné číslo organizácie.
Pre slovenské právnické osoby sa tu uvádza IČO, pre zahraničné právnické osoby ekvivalent z príslušného oficiálneho registra.
Dátum narodenia sa pri fyzických osobách zadáva v tvare RRRR-MM-DD, napríklad 1987-01-01.
Dátum narodenia nie je povinný údaj, ale pre presnejšiu identifikáciu Používateľa a najmä pre preukázanie nároku k Doméne odporúčame tento údaj vyplniť.

Poznámka
Formát dátumu sa bude v budúcnosti meniť na slovenský formát.

Príklad rožšírenia: Právnická osoba
<extension>
      <skContactIdent:create
        xmlns:skContactIdent="http://www.sk-nic.sk/xml/epp/sk-contact-ident-0.2">
      <skContactIdent:legalForm>CORP</skContactIdent:legalForm>
      <skContactIdent:identValue>
        <skContactIdent:corpIdent>1234567890</skContactIdent:corpIdent>
      </skContactIdent:identValue>
      </skContactIdent:create>
</extension>
Príklad rožšírenia: Fyzická osoba
<extension>
      <skContactIdent:create
        xmlns:skContactIdent="http://www.sk-nic.sk/xml/epp/sk-contact-ident-0.2">
      <skContactIdent:legalForm>PERS</skContactIdent:legalForm>
      </skContactIdent:create>
</extension>
Viac v <create> v časti EPP príkazy

Doplňujúce kontaktné informácie
Toto rozšírenie poskytuje bližšie kontaktné informácie o objekte. Jeho hlavným cieľom je doplnenie funkčnej doručovacej adresy spĺňajúcej podmienky podľa Pravidiel pre kontakty, ktoré príslušnú podmienku nespĺňajú. Celú dokumentáciu tohto rozšírenia nájdete na epp-auxcontact-extension.
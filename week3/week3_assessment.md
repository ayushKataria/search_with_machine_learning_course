# Answers for Questions of Week 3 Assignments:

## For classifying product names to categories:

### What precision (P@1) were you able to achieve?
0.886

### What fastText parameters did you use?
The best P@1 was achieved with the following settings:
1. min_products = 200
2. Learning Rate, lr=1.0 
3. epoch=25, 
4. wordNgrams=2

### How did you transform the product names?
1. Lowercased the names entirely
2. Removed all the characters other than alphanumeric ones and space
3. Stemmed each word of the product name using the NLTK Snowball Stemmer

### How did you prune infrequent category labels, and how did that affect your precision?
Loaded the all category labels and names to a pandas DataFrame, grouped them  by label and removed ones with lower values

### How did you prune the category tree, and how did that affect your precision?
I read all the category tree and created a dict with for each category it referred to the a list of categories with first element the root of that category and then going down the tree to last element. Then I replaced all the names with a specific depth, ie. 2 of the tree.

## For deriving synonyms from content:

### What 20 tokens did you use for evaluation?
```
    "products": ["headphones", "mobile", "laptop", "mouse", "tablet"],
    "brands": ["apple", "sony", "blackberry", "android", "lenovo"],
    "models": ["iphone", "thinkpad", "xbox", "walkman", "playstation"],
    "attribs": ["black", "large", "12GB", "cheap", "best"]
```

### What fastText parameters did you use?
minCount = default, 10, 20, 50

### How did you transform the product names?
Did the following in addition to the newline replacement that was already present:
1. Replcaed all the Registered(®), Trademark (™) and Copyright (©) symbols with white spaces.
2. Lowercased the names entirely
3. Removed all the punctuations

### What threshold score did you use? 
For most cases, a threshold of 0.90 looks decent.

### What synonyms did you obtain for those tokens?
Results obtained for minCount = 50:

1. headphones:
    1. ear 0.9109463691711426
    2. earbud 0.8767785429954529
    3. bud 0.8751177787780762
    4. skullcandy 0.8624414205551147
    5. sennheiser 0.8546338081359863
    6. stereo 0.7776666283607483
    7. head 0.7523476481437683
    8. headset 0.7509572505950928
    9. earbuds 0.7476560473442078
    10. clip 0.7447832822799683
2. mobile: 
    1. htc 0.9277914762496948
    2. 4g 0.8853462338447571
    3. blackberry 0.8759604692459106
    4. nokia 0.8558508157730103
    5. contract 0.8435015082359314
    6. invisibleshield 0.8319453597068787
    7. zagg 0.8288983702659607
    8. phones 0.8264628052711487
    9. motorola 0.8241428732872009
    10. unlocked 0.808768093585968
3. laptop: 
    1. laptops 0.8418955206871033
    2. aspire 0.8093534111976624
    3. pentium 0.8022761940956116
    4. i3 0.785493016242981
    5. inspiron 0.7798020839691162
    6. dell 0.7709372043609619
    7. i7 0.7648768424987793
    8. intel 0.7583216428756714
    9. lenovo 0.7550983428955078
    10. vaio 0.7529407739639282
4. mouse: 
    1.  optical 0.8513482809066772
    2.  savings 0.7922606468200684
    3.  keyscaper 0.78900146484375
    4.  98 0.7860809564590454
    5.  sales 0.7561039924621582
    6.  logitech 0.7386735677719116
    7.  instant 0.724452555179596
    8.  pad 0.7003133296966553
    9.  promark 0.6879101395606995
    10. wireless 0.683119535446167
5. tablet: 
    1.  tablets 0.8984584212303162
    2.  targus 0.7769421935081482
    3.  netbook 0.7528368234634399
    4.  acer 0.7363642454147339
    5.  atom 0.715365469455719
    6.  asus 0.7082907557487488
    7.  notebook 0.696980357170105
    8.  lenovo 0.68707674741745
    9.  3g 0.6850994229316711
    10. ipad 0.6637596487998962
___________________________________
TESTING brands
1. apple: 
    1.  ipod 0.8648110032081604
    2.  4th 0.828408420085907
    3.  dlo 0.817793071269989
    4.  incase 0.8105006814002991
    5.  iphone 0.8092876672744751
    6.  generation 0.7994648814201355
    7.  ipad 0.7861267328262329
    8.  folio 0.777116596698761
    9.  3rd 0.7762348055839539
    10. 4s 0.7703937888145447
2. sony: 
    1.  everio 0.6203808188438416
    2.  toshiba 0.6143597364425659
    3.  vaio 0.6128959655761719
    4.  digital 0.6122364401817322
    5.  alpha 0.601168692111969
    6.  handycam 0.5901956558227539
    7.  cyber 0.5853988528251648
    8.  jvc 0.5848950147628784
    9.  w 0.5840717554092407
    10. insignia 0.576130211353302
3. blackberry: 
    1.  htc 0.9015719890594482
    2.  mobile 0.8759604692459106
    3.  nokia 0.8736733198165894
    4.  4g 0.8607134819030762
    5.  otterbox 0.838801383972168
    6.  phones 0.8277878761291504
    7.  invisibleshield 0.8171407580375671
    8.  zagg 0.8155010938644409
    9.  motorola 0.8104776740074158
    10. unlocked 0.8076231479644775
4. android: 
    1.  biscuit 0.7456324696540833
    2.  self 0.739625871181488
    3.  side 0.7218297123908997
    4.  range 0.7210118174552917
    5.  freestanding 0.7187841534614563
    6.  bisque 0.7180444002151489
    7.  by 0.7172316312789917
    8.  water 0.7127537131309509
    9.  electrolux 0.7112230658531189
    10. microwave 0.7092791199684143
5. lenovo: 
    1.  aspire 0.895514726638794
    2.  inspiron 0.8902778625488281
    3.  i3 0.8667043447494507
    4.  acer 0.8574711084365845
    5.  i5 0.8565078973770142
    6.  gateway 0.855600893497467
    7.  i7 0.8525793552398682
    8.  pavilion 0.852326512336731
    9.  pentium 0.8487347960472107
    10. intel 0.8436369895935059

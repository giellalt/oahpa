readme for myv

1. sem classes prefixed with 'm' are for Morpha
   ==> hence useless at this moment!

src>g -h '<sem ' *|t
  15         <sem class="HUMAN_V"/>
  15             <sem class="FOOD_GROCERY"/>
   9         <sem class="mACTIVITY"/>
   9             <sem class="FOOD_DISH"/>
   8             <sem class="FOOD_A"/>
   7             <sem class="PLACE"/>
   7             <sem class="PEOPLE"/>
   7             <sem class="FAMILY"/>
   6             <sem class="DRINK"/>
   5         <sem class="FOODDRINK_V"/>
   5             <sem class="HUMAN_A"/>
   3         <sem class="MOVEMENT_V"/>
   3             <sem class="SETTLEMENT"/>
   3             <sem class="FOOD_GROCERY_PL"/>
   2             <sem class="mPERSNAME"/>
   1             <sem class="mMAL"/>
   1             <sem class="mFEM"/>
   1             <sem class="BIRD"/> 

2. sem classes in the src files should be adjusted to the
   classes as defined in the meta/semanticsets.xml
<lexicon>
  <subclasses class="HUMAN">  
    <sem class="PEOPLE"/>   
    <sem class="MYTH_BEING"/>   
    <sem class="FAMILY"/>
    <sem class="HUMAN_A"/>
    <sem class="HUMAN_V"/>
    <sem class="PLACE"/>
  </subclasses>
  <subclasses class="FOOD/DRINK">  
    <sem class="DRINK"/>
    <sem class="FOODDRINK_V"/>
    <sem class="FOOD_A"/>
    <sem class="FOOD_DISH"/>
    <sem class="FOOD_GROCERY"/>
  </subclasses>



# DATA PIPELINE ROUTE... (please disable the markdown... didn't want to spend more time formatting this tbh)

1. READ CSV FILE AS DATA FRAME  [DONE]

EXAMPLE OF A ROW AT THIS POINT: <br>
25/08/2021 09:00, Chesterfield,Richard Copeland, "Regular Flavoured iced latte - Hazelnut - 2.75, Large Latte - 2.45", 5.2, CARD, 5494173772652516

2. REMOVE THE COLUMNS NAME, CARD NUMBER [DONE]

EXAMPLE OF A ROW AT THIS POINT:  <br>
25/08/2021 09:00, Chesterfield, "Regular Flavoured iced latte - Hazelnut - 2.75, Large Latte - 2.45", 5.2, CARD


3. CHANGE DATE FORMAT TO POSTQGRE'S FORMAT [DONE]

EXAMPLE OF A ROW AT THIS POINT:  <br>

2021/08/25 09:00, Chesterfield,"Regular Flavoured iced latte - Hazelnut - 2.75, Large Latte - 2.45", 5.2, CARD


4. NORMALISE LOCATION AND PAYMENT_TYPE (A FUNCTION THAT CONNECTS TO DB AND CHECK IF THE LOCATION EXISTS RETURNING THE ID, IF NOT ADDS IT. SHOULD BE CREATED)

EXAMPLE OF A ROW AT THIS POINT:  <br>


2021/08/25 09:00, 1 ,"Regular Flavoured iced latte - Hazelnut - 2.75, Large Latte - 2.45", 5.2, 2


FOR PAYMENT TYPE

and a sql table named [payment_type] with 

payment_type_id, payment_type_name
        1               CASH
        2               CARD

A function that replaces CASH for 1 and CARD for 2 on each row needs to be done.

----

FOR LOCATION

A function that reads all the locations,location_id from the database as a dict needs to be implemented 

then we check the location column for each row against the dict... if it exist we will replace the name with the location_id number
if it doesn't, we have to insert the new location into the locations table, return the location_id for that insert and add it to the dict and continue the normalisation

[Location]

location_id   location_name
        1        Chesterfield
        2        Leeds

NOTE: maybe we should do this with payment_type aswell ... just in case we encounter a customer that pays with something like a CHEQUE or GIFTCARD later on


5. EXTRACT PRODUCTS FROM EACH ORDER AND ADD THEM TO A SEPARATE DATA FRAME WITH [ORDER_ID] [PRODUCT_NAME]

EXAMPLE OF A ROW AT THIS POINT: <br>

2021/08/25 09:00, 1 ,1, 5.2, 2  <br>

AND THIS WILL BE THE ORDER FOR SAID ROW  <br>

Regular Flavoured iced latte - Hazelnut - 2.75
Large Latte - 2.45


6. NORMALISE ORDER PRODUCTS (A FUNCTION THAT CONNECTS TO DB AND CHECK IF THE PRODUCT EXISTS RETURNING THE ID, IF NOT ADDS IT. SHOULD BE CREATED)

EXAMPLE OF A ROW AT THIS POINT: <br>

2021/08/25 09:00, 1 ,1, 5.2, 2 <br>

A table [order_products] will have the order_id and the product id <br>

order_id  product_id
    1        1
    1        2

A table [products] should be created 

product_id    product_name                               product_price
    1         Regular Flavoured iced latte - Hazelnut          2.75

all the relations should be made between those tables [this is done already in our schema]

NOTE: Just in case... the function that I made can separate Hazelnut to "flavors" if we need that bit later on


7. LOAD INTO DB

tbh... I would prefer to insert the bits into tables after each step and leave the orders one for last ... 
but if we're not meant to do it that way, then we will load everything here...

We'll use the class WithDB for this.... 

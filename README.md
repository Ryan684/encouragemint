# encouragemint

MVP:

POST plants
   - query takes plant name & garden as params and optional variety argument:
   - queries against trefle for that query plant name
   - if one response:
        - get plant_id from json object, load that.
            - if more than one variety:
                    if variety != none:
                        lookup variety by variety input:
                            if one result:
                                turn it into a model.
            return list of possible varieties
     else…
	return list of potential plants.


Future?

POST plants:
 - takes garden_id, loads garden details, makes suggestions based on environment.

- MVP slice - garden position (south facing etc). Make recommendation based on light requirements/shade?


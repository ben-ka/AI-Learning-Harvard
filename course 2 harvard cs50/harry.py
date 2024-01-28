from logic import *

rain = Symbol("rain") #it is raining
hagrid = Symbol("hagrid") # harry visited hagrid
dumbeldore = Symbol("dumbeldore") # harry visited dumbeldore

knowledge = And(
                Implication(Not(rain),hagrid)
                , Or(hagrid,dumbeldore),
                Not(And(hagrid,dumbeldore)),
                dumbeldore
                
                )

print(model_check(knowledge, rain))


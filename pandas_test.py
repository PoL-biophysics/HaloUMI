import pandas as pd

df = pd.DataFrame({
    "r": [],
    "vis": [],
    "area": [],
})


r = 400
vis = 20
area = 5000

row_to_add = pd.DataFrame([{"r": r, "vis": vis, "area": area}])

df = pd.concat([df, row_to_add], ignore_index=True)


print(df)
from Modules.utils import display_table
from Modules.db import db_getKey

user = db_getKey("users", "ibaan")
data = [["Sun",696000,1989100000],["Earth",6371,5973.6],["Moon",1737,73.5],["Mars",3390,641.85]]
display_table(data=data, tablefmt="plain")
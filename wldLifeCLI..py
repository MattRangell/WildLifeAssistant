from neo4j import GraphDatabase

class WildlifeCLI:
    def __init__(self, uri, user, password): 
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    # Operações CRUD para Animais
    def create_animal(self, name, habitat, comestivel,nomeFloresta):
        with self._driver.session() as session:
            session.write_transaction(self._create_animal, name, habitat, comestivel,nomeFloresta)

    def _create_animal(self, tx, name, habitat, comestivel, nomeFloresta):
        query = "CREATE (a:Animal {name: $name, habitat: $habitat, comestivel: $comestivel}) with a MATCH (l:Local {nome: &nomeFloresta}) CREATE (a)- [:PodeSerEncontrado]->(l)"
        tx.run(query, name=name, habitat=habitat, comestivel=comestivel, nomeFloresta=nomeFloresta)

    def read_animals(self):
        with self._driver.session() as session:
            return session.read_transaction(self._read_animals)

    def _read_animals(self, tx):
        query = "MATCH (a:Animal) RETURN a.name, a.habitat, a.comestivel"
        result = tx.run(query)
        return [{"name": record["a.name"], "habitat": record["a.habitat"], "comestivel": record["a.comestivel"]} for record in result]

    def update_animal(self, name, new_habitat):
        with self._driver.session() as session:
            session.write_transaction(self._update_animal, name, new_habitat)

    def _update_animal(self, tx, name, new_habitat):
        query = "MATCH (a:Animal {name: $name}) SET a.habitat = $new_habitat"
        tx.run(query, name=name, new_habitat=new_habitat)

    def delete_animal(self, name):
        with self._driver.session() as session:
            session.write_transaction(self._delete_animal, name)

    def _delete_animal(self, tx, name):
        query = "MATCH (a:Animal {name: $name}) DETACH DELETE a"
        tx.run(query, name=name)

    # Operações CRUD para Frutas
    def create_berry(self, name, comestivel, local_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_berry, name, comestivel, local_name)

    def _create_berry(self, tx, name, comestivel, local_name):
        query = "CREATE (b:Frutas {name: $name, comestivel: $comestivel}) with f MATCH (l:Local {nome: $local_name}) CREATE (b)-[:PodeSerEncontrado]->(l)"
        tx.run(query, name=name, comestivel=comestivel, local_name=local_name)

    def read_berries(self):
        with self._driver.session() as session:
            return session.read_transaction(self._read_berries)

    def _read_berries(self, tx):
        query = "MATCH (b:Frutas) RETURN b.name, b.comestivel"
        result = tx.run(query)
        return [{"name": record["b.name"], "comestivel": record["b.comestivel"]} for record in result]

    def update_berry(self, name, new_comestivel):
        with self._driver.session() as session:
            session.write_transaction(self._update_berry, name, new_comestivel)

    def _update_berry(self, tx, name, new_comestivel):
        query = "MATCH (b:Frutas {name: $name}) SET b.comestivel = $new_comestivel"
        tx.run(query, name=name, new_comestivel=new_comestivel)

    def delete_berry(self, name):
        with self._driver.session() as session:
            session.write_transaction(self._delete_berry, name)

    def _delete_berry(self, tx, name):
        query = "MATCH (b:Frutas {name: $name}) DETACH DELETE b"
        tx.run(query, name=name)

    # Operações CRUD para Locais
    def create_place(self, place_name, location, terreno, clima):
        with self._driver.session() as session:
         session.write_transaction(self._create_place, place_name, location, terreno, clima)

    def _create_place(self, tx, place_name, location, terreno, clima):
        query = "CREATE (p:Place {place_name: $place_name, location: $location, terreno: $terreno, clima: $clima})"
        tx.run(query, place_name=place_name, location=location, terreno=terreno, clima=clima)

    def read_places(self):
        with self._driver.session() as session:
            return session.read_transaction(self._read_places)

    def _read_places(self, tx):
        query = "MATCH (p:Place) RETURN p.place_name, p.location, p.terreno, p.clima"
        result = tx.run(query)
        return [{"place_name": record["p.place_name"], "location": record["p.location"], "terreno": ["p.terreno"], "clima": ["p.clima"]} for record in result]

    def update_place(self, place_name, new_location, new_terreno, new_clima):
        with self._driver.session() as session:
            session.write_transaction(self._update_place, place_name, new_location, new_terreno, new_clima)

    def _update_place(self, tx, place_name, new_location, new_terreno, new_clima):
        query = "MATCH (p:Place {place_name: $place_name}) SET p.location = $new_location, p.terreno = $new_terreno, p.clima = $new_clima"
        tx.run(query, place_name=place_name, new_location=new_location, new_terreno=new_terreno, new_clima=new_clima)

    def delete_place(self, place_name):
        with self._driver.session() as session:
            session.write_transaction(self._delete_place, place_name)

    def _delete_place(self, tx, place_name):
        query = "MATCH (p:Place {place_name: $place_name}) DETACH DELETE p"
        tx.run(query, place_name=place_name)

    def create_relationship(self, from_entity, to_entity, relationship_type):
        with self._driver.session() as session:
            session.write_transaction(self._create_relationship, from_entity, to_entity, relationship_type)
 
    def _create_relationship(self, tx, from_entity, to_entity, relationship_type):
        query = "MATCH (a:{from_entity.__class__.__name__}),(b:{to_entity.__class__.__name__}) WHERE a.name = $from_name AND b.name = $to_name CREATE (a)-[r:{relationship_type}]->(b)"
        tx.run(query, from_name=from_entity.name, to_name=to_entity.name, relationship_type=relationship_type)
 


# Exemplo de uso
if __name__ == "__main__":
    uri = "neo4j+s://e5f97f8e.databases.neo4j.io" ##URI, USER E PASSWORD setados de acordo com o ambiente de teste
    user = "neo4j"  
    password = "L6LaUIq2owcrImSJsoEtPN9qOhFpbkSXwlI-aD6kPDY" 

    cli = WildlifeCLI(uri, user, password)

    ## CRUD dos locais
    cli.create_place("Floresta Nustia Rowep","-2.24215, -156.75196","Floresta Densa","Temperado")
    cli.create_place("Campo Nhoj Kicw","58.23964, -87.81123","aberto", "Temperado")
    cli.create_place("Floresta nukemar", "-15.63725, -37.45536", "fechado", "boreal")

    places = cli.read_places()
    print("Places: ", places)

    cli.update_place("Floresta Nustia Rowep",": -54.07958, -92.74572", "Floresta Tropical", "Tropical")
    
    cli.delete_place("Floresta nukemar")


    # Operações CRUD para Animais
    cli.create_animal("Veado", "Floresta", True, "Floresta Nustia Rowep")
    cli.create_animal("Lontra","Floresta", True, "Floresta Nustia Rowep")
    cli.create_animal("Esquilo", "Floresta", False, "Floresta Nustia Rowep")
    cli.create_animal("Coelho", "Campo", True, "Campo Nhoj Kicw")
    cli.create_animal("Rato", "Campo", False, "Campo Nhoj Kicw")
    

    animals = cli.read_animals()
    print("Animals:", animals)
    
    cli.update_animal("Veado", "Campo")

    animals_after_update = cli.read_animals()
    print("Animals after update:", animals_after_update)

    cli.delete_animal("Veado")

    animals_after_delete = cli.read_animals()
    print("Animals after delete:", animals_after_delete)

    # Operações CRUD para Frutas
    cli.create_berry("Mirtilio", "Floresta", True, "Floresta Nustia Rowep")
    cli.create_berry("Morango Laturan", "Floresta", True, "Floresta Nustia Rowep")
    cli.create_berry("Jatropha", "Floresta", False, "Floresta Nustia Rowep")
    cli.create_berry("Framboesa", "Campo", True, "Campo Nhoj Kicw") 
    cli.create_berry("Elderberries", "Campo", False, "Campo Nhoj Kicw")
    cli.create_berry("Maca", "Campo", True, "Campo Nhoj Kicw") 

    berries = cli.read_berries()
    print("Berries:", berries)

    cli.update_berry("Morango Laturan",False)

    berries_after_update = cli.read_berries()
    print("Berries after update:", berries_after_update)

    cli.delete_berry("Morango")

    berries_after_delete = cli.read_berries()
    print("Berries after delete:", berries_after_delete)
    
    ##Criando relações

    cli.create_relationship(animals,berries,"Come")

    cli.close()
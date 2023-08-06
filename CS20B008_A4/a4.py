import xml.etree.ElementTree as ET
from owlready2 import *

# Load the ontology
ontology = get_ontology('a3.owl').load()

# Create a new ontology object for inferred triples
inferred_ontology = get_ontology('a3.owl')
inferred_ontology.load()

with inferred_ontology:
    # Define a new class for Room instances
    class RoomInstance(inferred_ontology.Room):
        pass

    # Infer triples
    sync_reasoner()

    # Save the inferred RDF triples to a file
    inferred_ontology.save(file='inferred.rdf', format='rdfxml')

    # Load the XML file
    xml_file = 'hotel.xml'
    xml_tree = ET.parse(xml_file)
    xml_root = xml_tree.getroot()

    # Extract room data and create RDF triples
    for room_elem in xml_root.findall('room'):
        room_no = room_elem.get('room_no')

        # Create individual of the RoomInstance class
        room_individual = RoomInstance(room_no)

# Save the extracted RDF triples to a file
inferred_ontology.save(file='extracted.rdf', format='rdfxml')

start_segment = '<RoomCost rdf:about="#20000">\n  <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#NamedIndividual"/>\n</RoomCost>'
end_segment = '<owl:AllDisjointClasses>\n  <owl:members rdf:parseType="Collection">\n    <rdf:Description rdf:about="#CarRental"/>\n    <rdf:Description rdf:about="#Ironing"/>\n    <rdf:Description rdf:about="#Laundry"/>\n    <rdf:Description rdf:about="#RoomCleaning"/>\n  </owl:members>\n</owl:AllDisjointClasses>'

with open('extracted.rdf', 'r') as file:
    rdf_content = file.read()

start_index = rdf_content.index(start_segment)
end_index = rdf_content.index(end_segment)

room_triples = room_triples = rdf_content[start_index + len(start_segment):end_index]
room_triples = room_triples.lstrip()

with open('rooms.rdf', 'w') as file:
    file.write(room_triples)

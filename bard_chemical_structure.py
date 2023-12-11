import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import Draw

# Define the SMILES string of the molecule
smiles = 'C1=CC=CC=C1'

# Convert the SMILES string to a molecule object
mol = Chem.MolFromSmiles(smiles)

# Draw the molecule
drawer = Draw.MolDraw2DSVG(width=300, height=300)
drawer.DrawMolecule(mol)
drawer.FinishDrawing()

# Display the molecule
plt.imshow(drawer.GetDrawingImage(), aspect='equal')
plt.axis('off')
plt.title('Chemical Structure')
plt.show()

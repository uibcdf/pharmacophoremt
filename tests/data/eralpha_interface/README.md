# Declared 1QKU fragment/EST interface

This case reuses the original bytes and acquisition declarations in
`../eralpha_rcsb/` and the reviewed EST chemical template in
`../eralpha_template/`. No prepared coordinates are substituted for the deposited
heavy atoms. `manifest.json` fixes the source checksum, fragment, chemical choices,
reviewed peptide graph and analytical modeling choices.

The receptor is label-chain A residues 304–550. SER301, PRO302 and LEU303 are
excluded because their observed heavy graphs are incomplete. Histidines are HIE;
the newly declared fragment termini are ammonium/carboxylate. These choices do
not establish the complete receptor, a pH-dependent state or a biological assembly.
Peptide stereo remains unspecified by the provider template. Local RDKit H
placement is not receptor/environment refinement.

The template-to-observed ARG NH1/NH2 name permutation is an explicit declaration
for this inspected source/template pair, retained with the complete map in the
recipe report. It is not automatic atom matching or a general resonance rule.
Changing the source or peptide graph checksum requires reviewing that map.

`devtools.prepare_eralpha_interface.prepare_interface()` uses public MolSysMT
operations and returns the prepared graph, original-atom maps and three separately
named detector analyses. `devtools.validate_eralpha_interface` composes existing
PharmacophoreMT tools and exercises independent placed-pose controls. Detector
parameters and evaluated coverage are retained, including zero H-bond/pi-pi
observations. The five ligand-reference sites remain a separate hypothesis source.

H5MSM preserves the native preparation history, including typed unknown numerical
entries and their original operation domains. The JSON evidence summarizes
aromatic normalization; its original integer/fractional orders remain in that
native history. JSON pharmacophore persistence is a separate consumer boundary.

This is local controlled-source integration evidence under PharmacophoreMT #22.
It makes no claim about affinity, biological enrichment, public package delivery,
performance, complete receptor preparation or refinement.

`diagnostics.json` separately declares candidate inspection and fixed criterion
comparisons for `devtools.diagnose_eralpha_interface`. It does not change the
original preparation, query or cached observations. The corresponding guard
`tests/test_eralpha_interaction_diagnostics.py` independently checks the recognized
nearby donor/H/acceptor triples and the frozen PHE404/EST reference intersection
rejection. No molecular geometry/refinement engine is implemented in this client.

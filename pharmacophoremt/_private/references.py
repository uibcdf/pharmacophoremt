"""Offline declarations checked against original project and publication records.

Sources: pyproject.toml; https://numpy.org/citing-numpy/;
https://scipy.org/citing-scipy/; SciPy linear_sum_assignment documentation;
https://pubmed.ncbi.nlm.nih.gov/17288412/. Checked 2026-10-02.
Clique implementation references: NetworkX find_cliques documentation,
https://networkx.org/documentation/stable/reference/algorithms/generated/
networkx.algorithms.clique.find_cliques.html. Checked 2026-10-03.
NetworkX software-description record: https://networkx.org/documentation/stable/#citing.
Provider-documented least-RMSD criterion: https://journals.iucr.org/paper?a12999
and MolSysMT structure.least_rmsd_fit docstring. Checked 2026-10-03.
RDP and pharmacophore clique papers remain design references, not executed methods.
G3PS section 2.2.1 was inspected in the primary paper, DOI
10.3390/molecules26237201, on 2026-10-03. Only its adapted neighborhood/guess
ranking and separately adapted section 2.2.2 refinement stages are implemented;
attribution contexts name the orientation policy and excluded stages.
"""

from copy import deepcopy
from sys import modules

ARTICLES = {
    "g3ps_seed_ranking": dict(
        id="pharmacophoremt:doi:10.3390/molecules26237201",
        type="article",
        title="Greedy 3-Point Search (G3PS)—A Novel Algorithm for Pharmacophore Alignment",
        authors=["Permann, Christian", "Seidel, Thomas", "Langer, Thierry"],
        journal="Molecules",
        year=2021,
        volume="26",
        number="23",
        pages="7201",
        doi="10.3390/molecules26237201",
    ),
    "kabsch": dict(
        id="pharmacophoremt:doi:10.1107/S0567739476001873",
        type="article",
        title="A solution for the best rotation to relate two sets of vectors",
        authors=["Kabsch, W."],
        journal="Acta Crystallographica Section A",
        year=1976,
        volume="32",
        pages="922–923",
        doi="10.1107/S0567739476001873",
    ),
    "networkx": dict(
        id="pharmacophoremt:networkx:paper:2008",
        type="inproceedings",
        title="Exploring network structure, dynamics, and function using NetworkX",
        authors=["Hagberg, Aric A.", "Schult, Daniel A.", "Swart, Pieter J."],
        booktitle="Proceedings of the 7th Python in Science Conference (SciPy2008)",
        year=2008,
        pages="11–15",
        url="https://networkx.org/documentation/stable/#citing",
    ),
    "bron_kerbosch": dict(
        id="pharmacophoremt:doi:10.1145/362342.362367",
        type="article",
        title="Algorithm 457: finding all cliques of an undirected graph",
        authors=["Bron, C.", "Kerbosch, J."],
        journal="Communications of the ACM",
        year=1973,
        volume="16",
        number="9",
        pages="575–577",
        doi="10.1145/362342.362367",
    ),
    "tomita_cliques": dict(
        id="pharmacophoremt:doi:10.1016/j.tcs.2006.06.015",
        type="article",
        title="The worst-case time complexity for generating all maximal cliques and computational experiments",
        authors=["Tomita, Etsuji", "Tanaka, Akira", "Takahashi, Haruhisa"],
        journal="Theoretical Computer Science",
        year=2006,
        volume="363",
        number="1",
        pages="28–42",
        doi="10.1016/j.tcs.2006.06.015",
    ),
    "numpy": dict(
        id="pharmacophoremt:doi:10.1038/s41586-020-2649-2",
        type="article",
        title="Array programming with NumPy",
        authors=[
            "Harris, Charles R.",
            "Millman, K. Jarrod",
            "van der Walt, Stéfan J.",
            "Gommers, Ralf",
            "Virtanen, Pauli",
            "Cournapeau, David",
            "Wieser, Eric",
            "Taylor, Julian",
            "Berg, Sebastian",
            "Smith, Nathaniel J.",
            "Kern, Robert",
            "Picus, Matti",
            "Hoyer, Stephan",
            "van Kerkwijk, Marten H.",
            "Brett, Matthew",
            "Haldane, Allan",
            "Fernández del Río, Jaime",
            "Wiebe, Mark",
            "Peterson, Pearu",
            "Gérard-Marchant, Pierre",
            "Sheppard, Kevin",
            "Reddy, Tyler",
            "Weckesser, Warren",
            "Abbasi, Hameer",
            "Gohlke, Christoph",
            "Oliphant, Travis E.",
        ],
        journal="Nature",
        year=2020,
        volume="585",
        pages="357–362",
        doi="10.1038/s41586-020-2649-2",
    ),
    "scipy": dict(
        id="pharmacophoremt:doi:10.1038/s41592-019-0686-2",
        type="article",
        title="SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python",
        authors=[
            "Virtanen, Pauli",
            "Gommers, Ralf",
            "Oliphant, Travis E.",
            "Haberland, Matt",
            "Reddy, Tyler",
            "Cournapeau, David",
            "Burovski, Evgeni",
            "Peterson, Pearu",
            "Weckesser, Warren",
            "Bright, Jonathan",
            "van der Walt, Stéfan J.",
            "Brett, Matthew",
            "Wilson, Joshua",
            "Millman, K. Jarrod",
            "Mayorov, Nikolay",
            "Nelson, Andrew R. J.",
            "Jones, Eric",
            "Kern, Robert",
            "Larson, Eric",
            "Carey, C J",
            "Polat, İlhan",
            "Feng, Yu",
            "Moore, Eric W.",
            "VanderPlas, Jake",
            "Laxalde, Denis",
            "Perktold, Josef",
            "Cimrman, Robert",
            "Henriksen, Ian",
            "Quintero, E. A.",
            "Harris, Charles R.",
            "Archibald, Anne M.",
            "Ribeiro, Antônio H.",
            "Pedregosa, Fabian",
            "van Mulbregt, Paul",
            "{SciPy 1.0 Contributors}",
        ],
        journal="Nature Methods",
        year=2020,
        volume="17",
        pages="261–272",
        doi="10.1038/s41592-019-0686-2",
    ),
    "assignment": dict(
        id="pharmacophoremt:doi:10.1109/TAES.2016.140952",
        type="article",
        title="On implementing 2D rectangular assignment algorithms",
        authors=["Crouse, David F."],
        year=2016,
        journal="IEEE Transactions on Aerospace and Electronic Systems",
        volume="52",
        number="4",
        pages="1679–1696",
        doi="10.1109/TAES.2016.140952",
    ),
    "bedroc": dict(
        id="pharmacophoremt:doi:10.1021/ci600426e",
        type="article",
        title='Evaluating virtual screening methods: good and bad metrics for the "early recognition" problem',
        authors=["Truchon, Jean-François", "Bayly, Christopher I"],
        year=2007,
        journal="Journal of Chemical Information and Modeling",
        volume="47",
        number="2",
        pages="488–508",
        doi="10.1021/ci600426e",
    ),
}

SOFTWARE = {
    "pharmacophoremt": ("PharmacophoreMT", "https://github.com/uibcdf/pharmacophoremt"),
    "numpy": ("NumPy", "https://numpy.org/"),
    "scipy": ("SciPy", "https://scipy.org/"),
    "molsysmt": ("MolSysMT", "https://github.com/uibcdf/molsysmt"),
    "pyunitwizard": ("PyUnitWizard", "https://github.com/uibcdf/pyunitwizard"),
    "networkx": ("NetworkX", "https://networkx.org/"),
}


def software_declarations(library):
    """Describe the actually loaded software version; never import a backend."""
    title, url = SOFTWARE[library]
    version = str(getattr(modules[library], "__version__", "unknown"))
    context = dict(software=library, version=version)
    record = dict(
        # Consumer-owned declarations cannot overwrite a provider's record.
        id=f"pharmacophoremt:software:{library}:{version}",
        type="software",
        title=title,
        version=version,
        url=url,
    )
    if library == "pharmacophoremt":
        record["authors"] = ["{UIBCDF Lab}"]  # Corporate author from pyproject.toml.
    declarations = [dict(record=record, roles=["executed_software"], context=context)]
    if library in {"numpy", "scipy", "networkx"}:
        declarations.append(
            dict(
                record=deepcopy(ARTICLES[library]),
                roles=["software_description"],
                context=context,
            )
        )
    return declarations


def criterion_declaration(name):
    context = dict(method=name)
    role = "scientific_criterion"
    if name.startswith("g3ps_refinement_"):
        context.update(
            paper_section="2.2.2",
            implemented_stage="greedy_pair_extension",
            orientation_policy=name.removeprefix("g3ps_refinement_"),
            adaptation="supplied_seed_mappings; best_fully_evaluated_state_retention; deterministic_ties; uniform_tolerances",
            excluded_stages="translation_rescue; exclusion_dodging; orientation_aware_fitting; seed_skipping",
        )
        role = "methodological_basis"
    elif name == "g3ps_seed_ranking":
        context.update(
            paper_section="2.2.1",
            implemented_stage="typed_neighborhood_comparison_and_multiple_guess_ranking",
            adaptation="uniform_position_tolerance; unit_cost_padding_for_unmatched_neighbors; deterministic_ties",
            excluded_stages="greedy_refinement; translation_rescue; exclusion_dodging",
        )
        role = "methodological_basis"
    if name == "kabsch":
        context.update(
            provider="molsysmt.structure.least_rmsd_fit",
            software="molsysmt",
            version=str(modules["molsysmt"].__version__),
            basis="provider_documented_least_rmsd_method",
        )
    if name == "assignment":
        # The referenced implementation is executed inside SciPy, not copied here.
        context.update(software="scipy", version=str(modules["scipy"].__version__))
        role = "reference_implementation"
    elif name in {"bron_kerbosch", "tomita_cliques"}:
        context.update(
            software="networkx", version=str(modules["networkx"].__version__)
        )
        role = "reference_implementation"
    article = "g3ps_seed_ranking" if name.startswith("g3ps_refinement_") else name
    return dict(record=deepcopy(ARTICLES[article]), roles=[role], context=context)

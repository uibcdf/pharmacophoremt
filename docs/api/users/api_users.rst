Users
=====

.. toctree::
   :name: users
   :caption: Users
   :maxdepth: 2

Incremental prepared-input screening
-----------------------------------

Available in development source. The
:doc:`prepared-input recipe </content/cookbook/prepared_incremental_screening>`
loads a saved native query, reads authorized prepared files through public
MolSysMT operations, consumes source-linked outcomes and exports them without
accumulating a molecular collection. See the recipe for supported execution
scope, reader ownership, score/failure semantics and qualification limits.

.. autoclass:: pharmacophoremt.screening.PreparedInput
   :members:

.. autofunction:: pharmacophoremt.screening.screen_prepared


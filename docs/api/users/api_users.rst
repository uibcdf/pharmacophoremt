Users
=====

.. toctree::
   :name: users
   :caption: Users
   :maxdepth: 2

Incremental prepared-input screening
------------------------------------

Available in development source. The
:doc:`prepared-input recipe </content/cookbook/prepared_incremental_screening>`
loads a saved native query, reads authorized prepared files through public
MolSysMT operations, consumes source-linked outcomes and exports them without
accumulating a molecular collection. See the recipe for supported execution
scope, reader ownership, score/failure semantics and qualification limits.

.. autoclass:: pharmacophoremt.screening.PreparedInput
   :members:

.. autofunction:: pharmacophoremt.screening.screen_prepared

.. autofunction:: pharmacophoremt.screening.reuse_feature_inventories

Recoverable prepared screening and saved results
------------------------------------------------

Selected source and bounded owned-wheel receiving pass; full supported/public
qualification remains separate. The
:doc:`recoverable recipe </content/cookbook/recoverable_prepared_screening>`
distinguishes immutable confirmations, new iterator deliveries and the complete
saved view. Independent reading uses the companion package in the same wheel.

The :doc:`plan inspection recipe </content/cookbook/prepared_run_plan_inspection>`
shows compact console display and PreparedRunPlan.describe(): exact query byte
identity plus detached original context, without reconstruction or a current
execution-compatibility decision.

.. autoclass:: pharmacophoremt.screening.PreparedRunPlan
   :members:

.. autofunction:: pharmacophoremt.screening.build_prepared_run_plan

.. autofunction:: pharmacophoremt.screening.resume_prepared_run

.. autoclass:: pharmacophoremt.screening.PreparedScreeningRun
   :members:

.. autoclass:: pharmacophoremt_results.ScreeningRunStore
   :members:

.. autoclass:: pharmacophoremt_results.ScreeningRunView
   :members:


Saved feature evidence
----------------------

The :doc:`feature-archive guide </content/user/feature_archives>` demonstrates
pinned metadata inspection, declared coverage and exact opaque original bytes.
Scientific quantity reconstruction and source/query admission remain separate.

.. autoclass:: pharmacophoremt_features.FeatureAssetView
   :members:

.. autoclass:: pharmacophoremt_features.FeatureAssetStore
   :members:

.. autoclass:: pharmacophoremt_features.FeatureInventoryPayload
   :members:

.. autoclass:: pharmacophoremt_features.FeatureAssetError

from __future__ import annotations

import typing
import uuid
from typing import TYPE_CHECKING

import orm
from anytree import NodeMixin

from hybrid_orm.config import settings
from hybrid_orm.models.constants import TableName

__all__ = ["HybridModel"]


class ReplicationDependency(NodeMixin):
    """ReplicationDependency orders foreign key dependencies for a model

    It does this in an ordered tree so that all dependencies data are
    replicated before the root data point is copied to other data registry
    thereby eliminating constraint errors. Dependencies are replicated from the
    bottom of the tree up to the root node
    """

    def __init__(self, parent: HybridModel, child: HybridModel):
        raise NotImplementedError("Yet to be writen")


class HybridMixin:
    """Hybrid cloud behaviours for multiregistry models"""

    registry: orm.ModelRegistry = orm.ModelRegistry(
        database=settings.LEADER_DB
    )
    secondary_registry: orm.ModelRegistry = orm.ModelRegistry(
        database=settings.OUTPOST_DB
    )
    outpost_mode: bool = settings.OUTPOST_MODE
    read_from: orm.ModelRegistry = registry
    fields: dict

    def replicate(self, force: bool = False) -> HybridModel:
        """Replicates database in registries if

        Returns:
            HybridModel
        """
        raise NotImplementedError("Yet to be written")

    @property
    def replication_dependencies(self) -> ReplicationDependency:
        """Returns an ordered tree of dependency datapoints to replicate"""
        raise NotImplementedError("Yet to be written")


class HybridModel(orm.Model, HybridMixin):
    pass

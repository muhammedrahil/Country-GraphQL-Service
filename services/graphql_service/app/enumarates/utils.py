from enum import Enum as PyEnum


class StatusEnum(PyEnum):
    DELETED = "deleted"
    ACTIVE = "active"
    DRAFT = "draft"
    INACTIVE = "inactive"

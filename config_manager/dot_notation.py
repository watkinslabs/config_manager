from types import SimpleNamespace
from typing import Dict, Any, List, Optional

class IterableNamespace(SimpleNamespace):
    """A SimpleNamespace that's also iterable and dict-like"""
    
    def __iter__(self):
        """Make the namespace iterable, returning (key, value) pairs"""
        for key, value in vars(self).items():
            yield key, value

    def __str__(self):
        """Override the string representation to look cleaner"""
        # Get the attributes
        attrs = vars(self)
        if not attrs:
            return '{}'
        
        # Format them as key-value pairs
        attr_str = ', '.join(f'{key}={value!r}' for key, value in attrs.items())
        return f'{{{attr_str}}}'
    
    def __repr__(self):
        """Override the repr to look cleaner"""
        return self.__str__()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key, returning default if not found (dict-like behavior)"""
        return vars(self).get(key, default)
    
    def keys(self):
        """Return keys (dict-like behavior)"""
        return vars(self).keys()
    
    def values(self):
        """Return values (dict-like behavior)"""
        return vars(self).values()
    
    def items(self):
        """Return items as (key, value) pairs (dict-like behavior)"""
        return vars(self).items()
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists (dict-like behavior)"""
        return key in vars(self)
    
    def __getitem__(self, key: str) -> Any:
        """Get item using bracket notation (dict-like behavior)"""
        attrs = vars(self)
        if key not in attrs:
            raise KeyError(key)
        return attrs[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set item using bracket notation (dict-like behavior)"""
        setattr(self, key, value)
    
    def update(self, other: Optional[Dict] = None, **kwargs) -> None:
        """Update namespace with dictionary or kwargs (dict-like behavior)"""
        if other is not None:
            if hasattr(other, 'items'):
                for key, value in other.items():
                    setattr(self, key, value)
            else:
                for key, value in other:
                    setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def pop(self, key: str, default: Any = None) -> Any:
        """Remove and return a value by key (dict-like behavior)"""
        attrs = vars(self)
        if key in attrs:
            value = attrs[key]
            delattr(self, key)
            return value
        return default
    
    def setdefault(self, key: str, default: Any = None) -> Any:
        """Get value by key, setting it to default if not found (dict-like behavior)"""
        if not hasattr(self, key):
            setattr(self, key, default)
        return getattr(self, key)
    
    def clear(self) -> None:
        """Remove all items (dict-like behavior)"""
        for key in list(vars(self).keys()):
            delattr(self, key)
    
    def copy(self) -> 'IterableNamespace':
        """Create a shallow copy (dict-like behavior)"""
        new_ns = IterableNamespace()
        new_ns.update(vars(self))
        return new_ns
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a regular dictionary"""
        return namespace_to_dict(self)

def dict_to_namespace(d):
    """
    Convert a dictionary to an IterableNamespace recursively
    allowing for dot notation access and iteration
    
    Args:
        d: Dictionary to convert
        
    Returns:
        IterableNamespace object or original value if not a dict
    """
    if not isinstance(d, dict):
        return d
    
    # Create a new IterableNamespace instead of SimpleNamespace
    namespace = IterableNamespace()
    
    # Convert each key-value pair and set as attribute
    for key, value in d.items():
        if isinstance(value, dict):
            # Recursively convert nested dictionaries
            setattr(namespace, key, dict_to_namespace(value))
        elif isinstance(value, list):
            # Convert dictionaries within lists
            new_list = []
            for item in value:
                if isinstance(item, dict):
                    new_list.append(dict_to_namespace(item))
                else:
                    new_list.append(item)
            setattr(namespace, key, new_list)
        else:
            setattr(namespace, key, value)
            
    return namespace

def namespace_to_dict(namespace: SimpleNamespace) -> Dict:
    """
    Convert a SimpleNamespace back to a dictionary recursively
    
    Args:
        namespace: SimpleNamespace to convert
        
    Returns:
        Dictionary representation of the namespace
    """
    if not isinstance(namespace, SimpleNamespace):
        return namespace
        
    result = {}
    for key, value in namespace.__dict__.items():
        if isinstance(value, SimpleNamespace):
            result[key] = namespace_to_dict(value)
        elif isinstance(value, list):
            new_list = []
            for item in value:
                if isinstance(item, SimpleNamespace):
                    new_list.append(namespace_to_dict(item))
                else:
                    new_list.append(item)
            result[key] = new_list
        else:
            result[key] = value
    return result

def deep_merge(target: Dict, source: Dict) -> Dict:
    """
    Recursively merge source dict into target dict
    
    Args:
        target: Target dictionary to merge into
        source: Source dictionary to merge from
        
    Returns:
        The merged dictionary
    """
    for key, value in source.items():
        if key in target and isinstance(value, dict) and isinstance(target[key], dict):
            deep_merge(target[key], value)
        else:
            target[key] = value
    return target
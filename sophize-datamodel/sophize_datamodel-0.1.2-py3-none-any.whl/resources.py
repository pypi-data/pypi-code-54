
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from enum import Enum


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class Citation:
    text_citation: Optional[str]

    def __init__(self, text_citation: Optional[str]) -> None:
        self.text_citation = text_citation

    @staticmethod
    def from_dict(obj: Any) -> 'Citation':
        assert isinstance(obj, dict)
        text_citation = from_union([from_str, from_none], obj.get("textCitation"))
        return Citation(text_citation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["textCitation"] = from_union([from_str, from_none], self.text_citation)
        return result


class User:
    handle: Optional[str]
    user_email: Optional[str]
    user_link: Optional[str]
    user_name: Optional[str]
    user_pic: Optional[str]

    def __init__(self, handle: Optional[str], user_email: Optional[str], user_link: Optional[str], user_name: Optional[str], user_pic: Optional[str]) -> None:
        self.handle = handle
        self.user_email = user_email
        self.user_link = user_link
        self.user_name = user_name
        self.user_pic = user_pic

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        handle = from_union([from_str, from_none], obj.get("handle"))
        user_email = from_union([from_str, from_none], obj.get("userEmail"))
        user_link = from_union([from_str, from_none], obj.get("userLink"))
        user_name = from_union([from_str, from_none], obj.get("userName"))
        user_pic = from_union([from_str, from_none], obj.get("userPic"))
        return User(handle, user_email, user_link, user_name, user_pic)

    def to_dict(self) -> dict:
        result: dict = {}
        result["handle"] = from_union([from_str, from_none], self.handle)
        result["userEmail"] = from_union([from_str, from_none], self.user_email)
        result["userLink"] = from_union([from_str, from_none], self.user_link)
        result["userName"] = from_union([from_str, from_none], self.user_name)
        result["userPic"] = from_union([from_str, from_none], self.user_pic)
        return result


class Argument:
    argument_text: Optional[str]
    conclusion: Optional[str]
    lookup_terms: Optional[List[str]]
    premises: Optional[List[str]]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, argument_text: Optional[str], conclusion: Optional[str], lookup_terms: Optional[List[str]], premises: Optional[List[str]], citations: Optional[List[Citation]], contributor: Optional[User], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.argument_text = argument_text
        self.conclusion = conclusion
        self.lookup_terms = lookup_terms
        self.premises = premises
        self.citations = citations
        self.contributor = contributor
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Argument':
        assert isinstance(obj, dict)
        argument_text = from_union([from_str, from_none], obj.get("argumentText"))
        conclusion = from_union([from_str, from_none], obj.get("conclusion"))
        lookup_terms = from_union([lambda x: from_list(from_str, x), from_none], obj.get("lookupTerms"))
        premises = from_union([lambda x: from_list(from_str, x), from_none], obj.get("premises"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Argument(argument_text, conclusion, lookup_terms, premises, citations, contributor, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["argumentText"] = from_union([from_str, from_none], self.argument_text)
        result["conclusion"] = from_union([from_str, from_none], self.conclusion)
        result["lookupTerms"] = from_union([lambda x: from_list(from_str, x), from_none], self.lookup_terms)
        result["premises"] = from_union([lambda x: from_list(from_str, x), from_none], self.premises)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


class Author:
    user: Optional[User]

    def __init__(self, user: Optional[User]) -> None:
        self.user = user

    @staticmethod
    def from_dict(obj: Any) -> 'Author':
        assert isinstance(obj, dict)
        user = from_union([User.from_dict, from_none], obj.get("user"))
        return Author(user)

    def to_dict(self) -> dict:
        result: dict = {}
        result["user"] = from_union([lambda x: to_class(User, x), from_none], self.user)
        return result


class Article:
    abstract_text: Optional[str]
    authors: Optional[List[Author]]
    beliefset: Optional[str]
    content: Optional[str]
    title: Optional[str]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, abstract_text: Optional[str], authors: Optional[List[Author]], beliefset: Optional[str], content: Optional[str], title: Optional[str], citations: Optional[List[Citation]], contributor: Optional[User], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.abstract_text = abstract_text
        self.authors = authors
        self.beliefset = beliefset
        self.content = content
        self.title = title
        self.citations = citations
        self.contributor = contributor
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Article':
        assert isinstance(obj, dict)
        abstract_text = from_union([from_str, from_none], obj.get("abstractText"))
        authors = from_union([lambda x: from_list(Author.from_dict, x), from_none], obj.get("authors"))
        beliefset = from_union([from_str, from_none], obj.get("beliefset"))
        content = from_union([from_str, from_none], obj.get("content"))
        title = from_union([from_str, from_none], obj.get("title"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Article(abstract_text, authors, beliefset, content, title, citations, contributor, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["abstractText"] = from_union([from_str, from_none], self.abstract_text)
        result["authors"] = from_union([lambda x: from_list(lambda x: to_class(Author, x), x), from_none], self.authors)
        result["beliefset"] = from_union([from_str, from_none], self.beliefset)
        result["content"] = from_union([from_str, from_none], self.content)
        result["title"] = from_union([from_str, from_none], self.title)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


class Beliefset:
    sub_beliefset_ptrs: Optional[List[str]]
    unsupported_proposition_ptrs: Optional[List[str]]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, sub_beliefset_ptrs: Optional[List[str]], unsupported_proposition_ptrs: Optional[List[str]], citations: Optional[List[Citation]], contributor: Optional[User], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.sub_beliefset_ptrs = sub_beliefset_ptrs
        self.unsupported_proposition_ptrs = unsupported_proposition_ptrs
        self.citations = citations
        self.contributor = contributor
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Beliefset':
        assert isinstance(obj, dict)
        sub_beliefset_ptrs = from_union([lambda x: from_list(from_str, x), from_none], obj.get("subBeliefsetPtrs"))
        unsupported_proposition_ptrs = from_union([lambda x: from_list(from_str, x), from_none], obj.get("unsupportedPropositionPtrs"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Beliefset(sub_beliefset_ptrs, unsupported_proposition_ptrs, citations, contributor, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["subBeliefsetPtrs"] = from_union([lambda x: from_list(from_str, x), from_none], self.sub_beliefset_ptrs)
        result["unsupportedPropositionPtrs"] = from_union([lambda x: from_list(from_str, x), from_none], self.unsupported_proposition_ptrs)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


class Project:
    abstract_text: Optional[str]
    description: Optional[str]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, abstract_text: Optional[str], description: Optional[str], citations: Optional[List[Citation]], contributor: Optional[User], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.abstract_text = abstract_text
        self.description = description
        self.citations = citations
        self.contributor = contributor
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Project':
        assert isinstance(obj, dict)
        abstract_text = from_union([from_str, from_none], obj.get("abstractText"))
        description = from_union([from_str, from_none], obj.get("description"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Project(abstract_text, description, citations, contributor, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["abstractText"] = from_union([from_str, from_none], self.abstract_text)
        result["description"] = from_union([from_str, from_none], self.description)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


class Language(Enum):
    INFORMAL = "INFORMAL"
    METAMATH_SET_MM = "METAMATH_SET_MM"


class MetaLanguage(Enum):
    INFORMAL = "INFORMAL"
    METAMATH = "METAMATH"


class Proposition:
    language: Optional[Language]
    lookup_terms: Optional[List[str]]
    meta_language: Optional[MetaLanguage]
    negative_statement: Optional[str]
    remarks: Optional[str]
    statement: Optional[str]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, language: Optional[Language], lookup_terms: Optional[List[str]], meta_language: Optional[MetaLanguage], negative_statement: Optional[str], remarks: Optional[str], statement: Optional[str], citations: Optional[List[Citation]], contributor: Optional[User], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.language = language
        self.lookup_terms = lookup_terms
        self.meta_language = meta_language
        self.negative_statement = negative_statement
        self.remarks = remarks
        self.statement = statement
        self.citations = citations
        self.contributor = contributor
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Proposition':
        assert isinstance(obj, dict)
        language = from_union([Language, from_none], obj.get("language"))
        lookup_terms = from_union([lambda x: from_list(from_str, x), from_none], obj.get("lookupTerms"))
        meta_language = from_union([MetaLanguage, from_none], obj.get("metaLanguage"))
        negative_statement = from_union([from_str, from_none], obj.get("negativeStatement"))
        remarks = from_union([from_str, from_none], obj.get("remarks"))
        statement = from_union([from_str, from_none], obj.get("statement"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Proposition(language, lookup_terms, meta_language, negative_statement, remarks, statement, citations, contributor, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["language"] = from_union([lambda x: to_enum(Language, x), from_none], self.language)
        result["lookupTerms"] = from_union([lambda x: from_list(from_str, x), from_none], self.lookup_terms)
        result["metaLanguage"] = from_union([lambda x: to_enum(MetaLanguage, x), from_none], self.meta_language)
        result["negativeStatement"] = from_union([from_str, from_none], self.negative_statement)
        result["remarks"] = from_union([from_str, from_none], self.remarks)
        result["statement"] = from_union([from_str, from_none], self.statement)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


class Term:
    alternate_phrases: Optional[List[str]]
    definition: Optional[str]
    language: Optional[Language]
    lookup_terms: Optional[List[str]]
    meta_language: Optional[MetaLanguage]
    phrase: Optional[str]
    primitive: Optional[bool]
    remarks: Optional[str]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, alternate_phrases: Optional[List[str]], definition: Optional[str], language: Optional[Language], lookup_terms: Optional[List[str]], meta_language: Optional[MetaLanguage], phrase: Optional[str], primitive: Optional[bool], remarks: Optional[str], citations: Optional[List[Citation]], contributor: Optional[User], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.alternate_phrases = alternate_phrases
        self.definition = definition
        self.language = language
        self.lookup_terms = lookup_terms
        self.meta_language = meta_language
        self.phrase = phrase
        self.primitive = primitive
        self.remarks = remarks
        self.citations = citations
        self.contributor = contributor
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Term':
        assert isinstance(obj, dict)
        alternate_phrases = from_union([lambda x: from_list(from_str, x), from_none], obj.get("alternatePhrases"))
        definition = from_union([from_str, from_none], obj.get("definition"))
        language = from_union([Language, from_none], obj.get("language"))
        lookup_terms = from_union([lambda x: from_list(from_str, x), from_none], obj.get("lookupTerms"))
        meta_language = from_union([MetaLanguage, from_none], obj.get("metaLanguage"))
        phrase = from_union([from_str, from_none], obj.get("phrase"))
        primitive = from_union([from_bool, from_none], obj.get("primitive"))
        remarks = from_union([from_str, from_none], obj.get("remarks"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Term(alternate_phrases, definition, language, lookup_terms, meta_language, phrase, primitive, remarks, citations, contributor, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["alternatePhrases"] = from_union([lambda x: from_list(from_str, x), from_none], self.alternate_phrases)
        result["definition"] = from_union([from_str, from_none], self.definition)
        result["language"] = from_union([lambda x: to_enum(Language, x), from_none], self.language)
        result["lookupTerms"] = from_union([lambda x: from_list(from_str, x), from_none], self.lookup_terms)
        result["metaLanguage"] = from_union([lambda x: to_enum(MetaLanguage, x), from_none], self.meta_language)
        result["phrase"] = from_union([from_str, from_none], self.phrase)
        result["primitive"] = from_union([from_bool, from_none], self.primitive)
        result["remarks"] = from_union([from_str, from_none], self.remarks)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result



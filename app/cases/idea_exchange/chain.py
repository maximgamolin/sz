from domain.idea_exchange.main import Idea, Chain
from domain.idea_exchange.types import IdeaID
from typing import Type
from dll.idea_exchange.uow import ChainUOW
from dal.idea_exchange.qo import IdeaQO, ChainQO, AuthorQO, ChainEditorQO
from exceptions.auth import PermissionDenied
from exceptions.idea_exchange import IdeaIsNotEdiatable
from cases.idea_exchange.dto import ChainLinkUserInputDTO


class ChainCase:

    def __init__(self, uow_cls: Type[ChainUOW]):
        self.uow = uow_cls()

    def create_chain(
            self,
            user_id: int,
            chain_name: str,
            user_chain_links: list[ChainLinkUserInputDTO]
    ):
        with self.uow:
            chain_editor_qo = ChainEditorQO()
            chain_editor = self.uow.fetch_chain_editor(chain_editor_qo)
            chain = Chain.initialize_new(chain_editor)
            user_chain_links.sort(key=lambda x: x.position_in_list)
            chain_links = [
                self.uow.convert_chain_link_dto_to_entity(i) for i in user_chain_links
            ]
            chain.validate_chain_links(chain_links)
            chain.replace_chain_links(chain_links)
            self.uow.add_chain_for_save(chain)
            self.uow.commit()

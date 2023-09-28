from typing import Type

from app.cases.idea_exchange.dto import ChainLinkUiDto
from app.dal.idea_exchange.qo import ChainEditorQO
from app.dll.idea_exchange.uow import ChainUOW
from app.domain.idea_exchange.main import Chain


class ChainCase:

    def __init__(self, uow_cls: Type[ChainUOW] = ChainUOW
        self.uow = uow_cls()

    def create_chain(
            self,
            user_id: int,
            chain_name: str,
            user_chain_links: list[ChainLinkUiDto]
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

    def build_chain(self):
        chain_qo = ChainQO(chain_id=chain_id)
        chain_dto: ChainDalDto = self.chain_repo.fetch_one(filter_params=chain_qo)
        chain_links = self._fetch_chain_chain_links(chain_dto.chain_id)
        accept_chain_link = self._fetch_one_chain_link(chain_link_id=chain_dto.accept_chain_link_id)
        reject_chain_link = self._fetch_one_chain_link(chain_link_id=chain_dto.reject_chain_link_id)
        user_qo = UserQO(user_id=chain_dto.author_id)
        user_author = self.user_repo.fetch_one(filter_params=user_qo)
        return Chain(
            chain_id=chain_dto.chain_id,
            chain_links=chain_links,
            author=ChainEditor.from_user(user_author),
            reject_chain_link=reject_chain_link,
            accept_chain_link=accept_chain_link,
            _meta_is_deleted=chain_dto.is_deleted
        )

    def chain_for_user_choices(self):


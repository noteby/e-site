from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
#
from backend.definer import request as req_model
from backend.definer import response as res_model
from backend.database.models import Note
from backend.deps import current_user, get_db
from backend.internal import note as note_itn
from backend.utils.errors.errorcode import ApiError
from backend.utils.errors.exceptions import ApiException

#
_tags = ['Note']
router = APIRouter(tags=_tags)
own_router = APIRouter(tags=_tags, dependencies=[Depends(current_user)])


@router.get('/list', response_model=res_model.NoteListRes)
def get_list(
        limit: int = Query(default=8),
        offset: int = Query(default=0),
        db: Session = Depends(get_db),
):
    note_list: list[Note] = note_itn.get_note_list(db, display=True, limit=limit, offset=offset)
    count = note_itn.get_note_count(db, display=True)
    return res_model.NoteListRes(
        count=count,
        list=[res_model.NoteBaseInfoRes(note_id=note.id,
                                        title=note.title,
                                        created_at=note.created_at,
                                        ) for note in note_list
              ],
    )


@router.get('/{note_id}', response_model=res_model.NoteInfoRes)
def get_detail(note_id: int, db: Session = Depends(get_db)):
    note = note_itn.get_note_by_id(db, note_id=note_id, display=True)
    if not note:
        raise ApiException(ApiError.note_not_exists)
    else:
        return res_model.NoteInfoRes(
            note_id=note.id,
            title=note.title,
            content=note.content,
            created_at=note.created_at,
        )


@own_router.get('/list', response_model=res_model.OwnNoteListRes)
def get_list_for_own(
        limit: int = Query(default=8),
        offset: int = Query(default=0),
        db: Session = Depends(get_db),
):
    note_list: list[Note] = note_itn.get_note_list(db, limit=limit, offset=offset)
    count = note_itn.get_note_count(db)
    return res_model.OwnNoteListRes(
        count=count,
        list=[res_model.OwnNoteBaseInfoRes(note_id=note.id,
                                           title=note.title,
                                           display=note.display,
                                           created_at=note.created_at,
                                           updated_at=note.updated_at,
                                           ) for note in note_list
              ],
    )


@own_router.get('/{note_id}', response_model=res_model.OwnNoteInfoRes)
def get_detail_for_own(note_id: int, db: Session = Depends(get_db)):
    note = note_itn.get_note_by_id(db, note_id=note_id)
    if not note:
        raise ApiException(ApiError.note_not_exists)
    else:
        return res_model.OwnNoteInfoRes(
            note_id=note.id,
            title=note.title,
            display=note.display,
            content=note.content,
            created_at=note.created_at,
            updated_at=note.updated_at,
        )


@own_router.post('/', response_model=res_model.NoteIDRes)
def create_by_own(req: req_model.CreateNoteReq, db: Session = Depends(get_db)):
    note = note_itn.create_note(db, **req.dict())
    return res_model.NoteIDRes(note_id=note.id)


@own_router.put('/{note_id}', response_model=res_model.NoteIDRes)
def update_by_own(note_id: int, req: req_model.UpdateNoteReq, db: Session = Depends(get_db)):
    note = note_itn.update_note(db, note_id=note_id, **req.dict())
    if not note:
        raise ApiException(ApiError.note_not_exists)
    else:
        return res_model.NoteIDRes(note_id=note.id)


@own_router.delete('/{note_id}', response_model=res_model.NoteIDRes)
def delete_by_own(note_id: int):
    return res_model.NoteIDRes(note_id=0)

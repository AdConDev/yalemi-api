''' Define the router for vote-related operations in the application. '''

from typing import Annotated, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select, col
from app.models import User, Vote, VoteCreate, VoteRead, May
from app import oauth2, database as db


unauth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )

forb_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You don't have enough permissions",
    headers={"WWW-Authenticate": "Bearer"},
    )

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)


@router.post(
    "/{may_id}", status_code=status.HTTP_201_CREATED, response_model=VoteRead
    )
def post_vote(
    may_id: int,
    create_vote: VoteCreate,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Route to create a Vote, if already exist, it tries to update.
    Upvote, downvote, or neutral vote. '''
    # Validate user
    if not current_user:
        raise unauth_exception
    # It gets the May with the id may_id
    edited_may: Optional[May] = session.get(May, may_id)
    # If there is no May with that id, it raises an exception
    if not edited_may:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No May with ID {may_id} found"
            )
    # Checks if a vote with the same username and may already exists in the
    # database
    vote_in_db: Optional[Vote] = session.exec(
            select(Vote).where(
                col(Vote.user_id) == current_user.id,
                col(Vote.may_id) == may_id
                )).first()
    # If exists and user tries to put the same vote, it raises an exception
    if vote_in_db:
        if vote_in_db.vote_type == create_vote.vote_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vote already exists"
            )
        # If vote exists but user tries to change the vote, it updates the vote
        vote_in_db.vote_type = create_vote.vote_type
        session.add(vote_in_db)
        session.commit()
        session.refresh(vote_in_db)
        return vote_in_db
    # If vote doesn't exists, it creates a new Vote with the data from may_id
    # and the user_id of current_user
    new_vote = Vote.model_validate(create_vote, from_attributes=True)
    new_vote.user_id = current_user.id
    new_vote.may_id = may_id
    session.add(new_vote)
    session.commit()
    session.refresh(new_vote)
    return new_vote


@router.get("/", response_model=list[VoteRead])
def get_all_votes(
    *,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Route to get all Votes '''
    # Validate user
    if not current_user:
        raise unauth_exception
    # It gets all Votes
    all_votes = session.exec(select(Vote)).all()
    # If there are no Votes, it raises an exception
    if not all_votes:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No Votes yet"
            )
    return all_votes


@router.delete("/{may_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vote(
    may_id: int,
    current_user: Annotated[User, Depends(oauth2.get_current_active_user)],
    session: Session = Depends(db.get_session)
):
    ''' Route to delete a specific Vote '''
    # Validate user
    if not current_user:
        raise unauth_exception
    # It gets the Vote with the may id and current user id
    deleted_vote: Optional[Vote] = session.exec(
        select(Vote).where(
            Vote.user_id == current_user.id, Vote.may_id == may_id
            )
        ).first()
    # If there is no Vote with that may_id/user_id, it raises an exception
    if not deleted_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No vote with this user_id or may_id {may_id}"
        )
    # It deletes the Vote and returns nothing.
    session.delete(deleted_vote)
    session.commit()

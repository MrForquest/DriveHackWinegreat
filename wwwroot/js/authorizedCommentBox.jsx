class AuthorizedCommentBox extends CommentBox {
    render() {
        return (
            <>
                <div id="clocks">
                    <RealtimeClock />
                </div>
                <br />
                <div className="commentBox">
                    <CommentList data={this.state.data} />
                    <CommentForm onCommentSubmit={this.handleCommentSubmit} />
                </div>
            </>

        );
    }
}
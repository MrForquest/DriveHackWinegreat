class CommentBox extends React.Component {
	state = { data: undefined, intervalId: 0, lastId: 0 };
	//------------
	loadComments = () => {
		fetch(this.props.url, { method: "post", body: this.state.lastId, cache: "no-store", headers: { "content-type": "application/json" } }).then(x => {
			x.json().then(result => {
				if (result.result == 1)
					this.setState({ data: this.state.data.concat(result.data), lastId: result.lastId })
			})
		});
	};
	loadFirstComments = () => {
		fetch(this.props.url, { method: "post", body: 0, cache: "no-store", headers: { "content-type": "application/json" } }).then(x =>
			x.json().then(result => this.setState({ data: (result.data), lastId: result.lastId })));
	};
	//------------
	componentDidMount() {
		this.loadFirstComments();
		this.setState({ intervalId: setInterval(this.loadComments, 10000) });
	}
	componentWillUnmount() {
		clearInterval(this.state.intervalId);
	}
	//------------
	handleCommentSubmit = comment => {
		comment.id = 2;
		var formData = new FormData();
		formData.append('id', comment.id); formData.append('author', comment.author); formData.append('text', comment.text);
		fetch(this.props.submitUrl, { method: "post", body: formData });
	};
	//------------
	render() {
		return (
			<>
				<div>
					You did not Authorize! <br /> Can not make new post's yet
				</div>
				<div id="clocks">
					<RealtimeClock />
				</div>
				<br />
				<div className="commentBox">
					<CommentList data={this.state.data} />
				</div>
			</>

		);
	}
}

class CommentList extends React.Component {
	render() {
		if (this.props.data == undefined)
			return <div className="commentList">No Commentary</div>;
		var commentNodes = this.props.data.map(comment => (
			<Comment author={comment.author} key={comment.id}>
				{comment.text}
			</Comment>
		));
		return <div className="commentList">{commentNodes}</div>;
	}
}


class CommentForm extends React.Component {
	state = {
		author: '',
		text: ''
	};

	handleAuthorChange = e => {
		this.setState({ author: e.target.value });
	};

	handleTextChange = e => {
		this.setState({ text: e.target.value });
	};

	handleSubmit = e => {
		e.preventDefault();
		var author = this.state.author.trim();
		var text = this.state.text.trim();
		if (!text || !author) {
			return;
		}
		this.props.onCommentSubmit({ author: author, text: text });
		this.setState({ text: '' });
	};

	render() {
		return (
			<form className="commentForm" onSubmit={this.handleSubmit}>
				<input
					type="text"
					placeholder="Your name"
					value={this.state.author}
					onChange={this.handleAuthorChange}
				/>
				<div>
					<textarea placeholder="Say something..." onChange={this.handleTextChange} value={this.state.text} />
				</div>
				<input type="submit" value="Post" />
			</form>
		);
	}
}

function createRemarkable() {
	var remarkable =
		'undefined' != typeof global && global.Remarkable
			? global.Remarkable
			: window.Remarkable;

	return new remarkable();
}

class Comment extends React.Component {
	rawMarkup = () => {
		var md = createRemarkable();
		var rawMarkup = md.render(this.props.children.toString());
		return { __html: rawMarkup };
	};

	render() {
		return (
			<div className="comment">
				<h2 className="commentAuthor">{this.props.author}</h2>
				<span dangerouslySetInnerHTML={this.rawMarkup()} />
			</div>
		);
	}
}
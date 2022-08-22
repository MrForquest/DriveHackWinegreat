class RealtimeClock extends React.Component {

	state = { time: getTime(), intervalId: 0 };
	loadServerTime = () => {
		this.setState({ time: getTime() });
	}

	componentDidMount() {
		this.setState({ intervalId: setInterval(this.loadServerTime, 1000) });
	}
	componentWillUnmount() {
		clearInterval(this.state.intervalId);
	}

	render() {
		return (
			<div className="realtimeClock">
				<h3>Время сейчас:</h3>
				{this.state.time}
			</div>
		);
	}
}
function getTime() {

	return new Date().toLocaleTimeString();
}

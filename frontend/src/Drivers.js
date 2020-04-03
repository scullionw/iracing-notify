import React, { useState, useEffect } from 'react';

class Clock extends React.Component {
    constructor(props) {
        super(props);
        this.state = { date: new Date() };
    }

    componentDidMount() {
        this.timerID = setInterval(
            () => this.tick(),
            1000
        );
    }

    componentWillUnmount() {
        clearInterval(this.timerID);
    }

    tick() { this.setState({ date: new Date() }); }

    render() {
        return (
            <div>
                <h2>{this.state.date.toLocaleTimeString()}.</h2>
            </div>
        );
    }
}

function ClockH(props) {

    const [date, setDate] = useState(new Date());

    let timerID = null;

    useEffect(() => {
        componentDidMount();

        return componentWillUnmount;
    }, [])

    function componentDidMount() {
        timerID = setInterval(
            () => tick(),
            1000
        );
        console.log("Started timer!")
        // setTimerID(timerID);
    }

    function componentWillUnmount() {
        clearInterval(timerID);
        console.log("Clear timer!")
    }

    function tick() { setDate(new Date()) }


    return (
        <div>
            <h2>{date.toLocaleTimeString()}.</h2>
        </div>
    );

}



let NAMES = [
    "Max Verstappen",
    "Lando Norris",
];

function Driver(props) {
    return <li>{props.name}</li>
}

export default function Drivers() {

    let [count, setCount] = useState(0);



    useEffect(() => {
        const timer = setInterval(() => setCount(count + 1), 1000);
        console.log("Started name timer!")

        return () => {
            clearInterval(timer);
            console.log("Stopped name timer!")
        }
    })


    const drivers = NAMES.map((n) => <Driver key={n} name={n} />);

    return (
        <div>
            <ClockH />
            <h1>Currently Driving</h1>
            <ul>
                {drivers}
                <li>{count}</li>
            </ul>
        </div>

    );
}

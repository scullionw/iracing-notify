import React, { useState, useEffect } from 'react';


function Driving(props) {
    return (
        <DriverList status="Online" drivers={props.drivers} />
    );
}

function Offline(props) {
    return (
        <DriverList status="Offline" drivers={props.drivers} />
    );
}

function Driver(props) {
    return <li>{props.name}</li>
}

function DriverList(props) {
    const elements = props.drivers.map(d => <Driver key={d.name} name={d.name} />);
    return (
        <div>
            <h2>{props.status}</h2>
            <ul>{elements}</ul>
        </div>
    );
}


export default function Drivers() {
    const [status, setStatus] = useState(null);

    useEffect(() => {
        async function load_drivers() {
            let resp = await fetch("/api/drivers");
            let data = await resp.json();
            setStatus(data);
            console.log("Called!");
        }

        load_drivers();

        const timer = setInterval(load_drivers, 1000);

    }, []);

    let online = [];
    let offline = [];

    if (status === null) {
        return null;
    }

    status.forEach(driver => (driver.driving === null ? offline : online).push(driver));

    return (
        <>
            <h1>Driver status</h1>
            <Driving drivers={online} />
            <Offline drivers={offline} />
        </>
    );
}



import React, { useState, useEffect } from "react";
import partition from "lodash/partition";
import styles from "@emotion/styled";

function Driving(props) {
    return <DriverList status="Online" drivers={props.drivers} />;
}

function Offline(props) {
    return <DriverList status="Offline" drivers={props.drivers} />;
}

function Driver(props) {
    return <li>{props.name}</li>;
}

function DriverList({ drivers, status }) {
    const elements = drivers.map((d) => <Driver key={d.name} name={d.name} />);
    return (
        <div>
            <h2>{status}</h2>
            <ul>{elements}</ul>
        </div>
    );
}

export default function Drivers() {
    const [status, setStatus] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        async function load_drivers() {
            let resp = await fetch("/api/drivers");
            let data = await resp.json();
            setStatus(data);
            setIsLoaded(true);
        }

        load_drivers();

        const timer = setInterval(load_drivers, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    if (!isLoaded) {
        return null;
    }

    const [offline, online] = partition(
        status,
        (driver) => driver.driving === null
    );

    return (
        <div id="drivers">
            <h1>Driver status</h1>
            <Driving drivers={online} />
            <Offline drivers={offline} />
        </div>
    );
}

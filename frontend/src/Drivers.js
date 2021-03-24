import React, { useState, useEffect } from "react";
import partition from "lodash/partition";
import styled from "@emotion/styled";
import {
    Typography,
    ListItem,
    ListItemText,
    Card,
    Grid,
} from "@material-ui/core";

function Driver({ info }) {
    return (
        <Grid item>
            <Card>
                <ListItem>
                    <ListItemText
                        primary={`${info.name}`}
                        secondary={info.driving && extra_info(info)}
                    />
                </ListItem>
            </Card>
        </Grid>
    );
}

function extra_info(info) {
    return `${info.driving.series} - ${info.driving.session_type}`;
}

function DriverList({ drivers, status }) {
    const elements = drivers.map((d) => <Driver key={d.name} info={d} />);
    return (
        <div>
            <Typography variant="h5">
                <b>{status}</b>
            </Typography>
            <br />
            <Grid
                container
                direction="column"
                justify="center"
                alignItems="stretch"
                spacing={1}
            >
                {elements}
            </Grid>
            <br />
        </div>
    );
}

const CenteredTitle = styled(Typography)`
    text-align: center;
`;

const DriverContainer = styled.div`
    padding: 10px;
`;

const WarningTitle = styled(CenteredTitle)`
    color: red;
`;

function APIResults({ error, content }) {
    if (error) {
        return (
            <>
                <br />
                <WarningTitle variant="h5">API is down</WarningTitle>
            </>
        );
    } else {
        const [online, offline] = partition(content, (d) => d.driving);
        return (
            <>
                <DriverList status="Online" drivers={online} />
                <DriverList status="Offline" drivers={offline} />
            </>
        );
    }
}

export default function Drivers() {
    const [status, setStatus] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function get_drivers() {
            let resp = await fetch("./api/drivers");
            let data = await resp.json();
            setStatus(data);
            setError(null);
            setIsLoaded(true);
        }

        function load() {
            get_drivers().catch((error) => {
                console.log(error);
                setError(error);
                setIsLoaded(true);
            });
        }

        const timer = setInterval(load, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    if (!isLoaded) {
        return null;
    }

    return (
        <DriverContainer>
            <CenteredTitle variant="h2">Drivers</CenteredTitle>
            <APIResults error={error} content={status} />
        </DriverContainer>
    );
}

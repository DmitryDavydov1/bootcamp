import {useEffect, useState} from "react";
import SortableShelf from "./SortableShelf";

export default function Results({data}) {
    const [carousel, setCarousel] = useState([]);
    const [top10, setTop10] = useState([]);
    const [hot, setHot] = useState([]);

    useEffect(() => {
        if (!data) return;

        setCarousel(data.carousel || []);
        setTop10(data.top10 || []);
        setHot(data.hot || []);
    }, [data]);

    return (
        <div style={{padding: 20}}>
            <SortableShelf
                title="Carousel"
                items={carousel}
                setItems={setCarousel}
            />

            <SortableShelf
                title="Top 10"
                items={top10}
                setItems={setTop10}
            />

            <SortableShelf
                title="Hot"
                items={hot}
                setItems={setHot}
            />
        </div>
    );
}      
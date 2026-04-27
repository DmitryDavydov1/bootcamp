import {useEffect, useState} from "react";
import SortableShelf from "./SortableShelf";
import {getCurrentTop, saveCurrentTop} from "../api/client";

export default function Results({data}) {
    const [carousel, setCarousel] = useState([]);
    const [top10, setTop10] = useState([]);
    const [hot, setHot] = useState([]);
    const [currentTop, setCurrentTop] = useState(null);

    useEffect(() => {
        if (!data) return;

        setCarousel(data.carousel || []);
        setTop10(data.top10 || []);
        setHot(data.hot || []);
    }, [data]);

    useEffect(() => {
        loadCurrentTop();
    }, []);

    const loadCurrentTop = async () => {
        const res = await getCurrentTop();
        setCurrentTop(res.data);
    };

    const handleSave = async () => {
        const res = await saveCurrentTop({
            carousel,
            top10,
            hot,
        });

        setCurrentTop(res.data);
    };

    return (
        <div>
            <h2>Отчет</h2>

            <button onClick={handleSave}>
                Сохранить порядок
            </button>

            <SortableShelf title="Carousel" items={carousel} setItems={setCarousel}/>
            <SortableShelf title="Top 10" items={top10} setItems={setTop10}/>
            <SortableShelf title="Hot" items={hot} setItems={setHot}/>

            <hr/>

            <h2>Текущий топ</h2>

            {!currentTop || !currentTop.saved_at ? (
                <p>Пока ничего не сохранено</p>
            ) : (
                <div>
                    <p>
                        Сохранено: {new Date(currentTop.saved_at).toLocaleString()}
                    </p>

                    <TopPreview title="Carousel" items={currentTop.carousel}/>
                    <TopPreview title="Top 10" items={currentTop.top10}/>
                    <TopPreview title="Hot" items={currentTop.hot}/>
                </div>
            )}
        </div>
    );
}

function TopPreview({title, items}) {
    return (
        <div>
            <h3>{title}</h3>

            <ol>
                {items.map((item, index) => (
                    <li key={`${title}-${item.title}-${index}`}>
                        {item.title}
                    </li>
                ))}
            </ol>
        </div>
    );
}
export default function Results({data}) {
    console.log(data);
    const renderCards = (items, fields) => (
        <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
            gap: 16
        }}>
            {items.map((item, i) => (
                <div key={i} style={{
                    border: "1px solid #ddd",
                    borderRadius: 12,
                    padding: 16,
                    boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
                    background: "#fff"
                }}>
                    <h3 style={{fontSize: 16}}>{item.title}</h3>

                    {fields.map(f => (
                        <div key={f} style={{fontSize: 14, marginTop: 4}}>
                            <b>{f}:</b> {item[f]}
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );

    return (
        <div style={{padding: 20, background: "#f5f5f5"}}>

            <h2>🎠 Carousel</h2>
            {renderCards(data.carousel, [
                "ctr_carousel", "views", "bwr", "carousel_score"
            ])}

            <h2 style={{marginTop: 40}}>🏆 Top 10</h2>
            {renderCards(data.top10, [
                "views", "depth", "bwr", "top10_score"
            ])}

            <h2 style={{marginTop: 40}}>🔥 Hot</h2>
            {renderCards(data.hot, [
                "ctr_feed", "source_feed", "bwr", "views", "hot_score"
            ])}

        </div>
    );
}
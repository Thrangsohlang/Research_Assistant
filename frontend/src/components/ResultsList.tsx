export type Hit = {
    id: string;
    score: number;
    metadata: { source_doc_id: string; section_heading: string};
    document: string;
};

export default function ResultsList({ hits }: { hits: Hit[] }) {
    // if (!hits.length) return <p>No results yet</p>;
    
    return (
        <div>
            {hits.map(hit => (
                <div key={hit.id} style={{ padding: '16px', borderBottom: '1px solid #ddd' }}>
                    <h4>
                        {hit.metadata.source_doc_id} - {hit.metadata.section_heading}{' '}
                        <small>(score: {hit.score.toFixed(2)})</small>
                    </h4>
                    <p>{hit.document}</p>
                </div>
            ))}
        </div>
    );
}
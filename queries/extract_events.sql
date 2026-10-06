SELECT document_ref,
       status,
       changed_at,
       changed_by
FROM document_status_history
WHERE changed_at >= :from_date
ORDER BY document_ref, changed_at;

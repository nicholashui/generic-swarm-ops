# Frontend API Contract Notes

- Backend base URL defaults to `http://127.0.0.1:8000/api/v1`.
- Frontend is designed to tolerate current raw success payloads plus structured backend error envelopes.
- Workflow run realtime updates use the backend SSE run events endpoint.
- API generation output is stored in `src/lib/api/generated/`.

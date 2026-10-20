import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { api } from "./api.js";
import "./styles.css";

const sections = [
  ["overview", "Overview", "◫"],
  ["alerts", "Alerts", "◈"],
  ["cases", "Cases", "▣"],
  ["events", "Events", "⌁"],
];

const roleCanManage = (role) =>
  ["SENIOR_ANALYST", "INCIDENT_RESPONDER", "SOC_MANAGER", "ADMINISTRATOR"].includes(role);

function date(value) {
  if (!value) return "—";
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : parsed.toLocaleString();
}

function statusClass(value) {
  return "pill " + String(value || "").toLowerCase().replaceAll("_", "-");
}

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setError("");
    setBusy(true);
    try {
      const result = await api.login(username, password);
      localStorage.setItem("soc_token", result.access_token);
      onLogin(result.user);
    } catch (err) {
      setError(err.message || "Could not sign in.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="login-page">
      <div className="login-card">
        <div className="brand-mark">S</div>
        <p className="eyebrow">SECURITY OPERATIONS</p>
        <h1>Welcome back</h1>
        <p className="muted">Sign in to your SOC workspace.</p>
        <form onSubmit={submit} className="stack" style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
          <label style={{ display: "flex", flexDirection: "column", gap: "6px", width: "100%" }}>Username<input autoComplete="username" value={username} onChange={(e) => setUsername(e.target.value)} required /></label>
          <label style={{ display: "flex", flexDirection: "column", gap: "6px", width: "100%" }}>Password<input type="password" autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} required /></label>
          {error && <div className="error-box">{error}</div>}
          <button className="button primary full" disabled={busy}>{busy ? "Signing in…" : "Sign in"}</button>
        </form>
        <p className="login-foot">SOC Platform · Analyst console</p>
      </div>
    </main>
  );
}

function App() {
  const [user, setUser] = useState(null);
  const [checking, setChecking] = useState(Boolean(localStorage.getItem("soc_token")));
  const [page, setPage] = useState("overview");
  const [selectedCaseId, setSelectedCaseId] = useState(null);
  const [query, setQuery] = useState("");
  const [cases, setCases] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [events, setEvents] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const visibleCases = useMemo(() => cases.filter((item) => JSON.stringify(item).toLowerCase().includes(query.toLowerCase())), [cases, query]);
  const visibleAlerts = useMemo(() => alerts.filter((item) => JSON.stringify(item).toLowerCase().includes(query.toLowerCase())), [alerts, query]);
  const visibleEvents = useMemo(() => events.filter((item) => JSON.stringify(item).toLowerCase().includes(query.toLowerCase())), [events, query]);

  useEffect(() => {
    if (!localStorage.getItem("soc_token")) return;
    api.me().then(setUser).catch(() => {
      localStorage.removeItem("soc_token");
      setUser(null);
    }).finally(() => setChecking(false));
  }, []);

  async function refresh() {
    setBusy(true);
    setError("");
    try {
      if (page === "overview" || page === "cases") {
        const result = await api.cases();
        setCases(result.cases || []);
      }
      if (page === "overview" || page === "alerts") {
        const result = await api.alerts();
        setAlerts(result.alerts || []);
      }
      if (page === "overview" || page === "events") {
        const result = await api.events();
        setEvents(result.events || []);
      }
    } catch (err) {
      setError(err.message || "Could not load SOC data.");
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => {
    if (user) refresh();
  }, [page, user]);

  async function openCase(id) {
    setSelectedCaseId(id);
    setError("");
    try {
      const [caseResult, timelineResult] = await Promise.all([api.case(id), api.timeline(id)]);
      setSelectedCase(caseResult.case);
      setTimeline(timelineResult.timeline || []);
    } catch (err) {
      setError(err.message || "Could not load case.");
    }
  }

  async function reloadSelectedCase() {
    if (selectedCaseId) await openCase(selectedCaseId);
    await refresh();
  }

  function signOut() {
    localStorage.removeItem("soc_token");
    setUser(null);
    setSelectedCaseId(null);
    setSelectedCase(null);
  }

  if (checking) return <div className="loading-screen"><span className="spinner" />Checking session…</div>;
  if (!user) return <Login onLogin={setUser} />;

  const title = selectedCaseId ? "Investigation" : sections.find(([key]) => key === page)?.[1] || "Overview";

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand"><div className="brand-mark small">S</div><div><strong>SOC<span>PLATFORM</span></strong><small>SECURITY OPERATIONS</small></div></div>
        <div className="side-label">WORKSPACE</div>
        <nav>
          {sections.map(([key, label, icon]) => (
            <button key={key} className={"nav-item " + (!selectedCaseId && page === key ? "active" : "")} onClick={() => { setSelectedCaseId(null); setSelectedCase(null); setPage(key); }}>
              <span className="nav-icon">{icon}</span>{label}
              {key === "alerts" && alerts.filter((a) => a.status === "NEW").length > 0 && <span className="nav-count">{alerts.filter((a) => a.status === "NEW").length}</span>}
            </button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="connection"><span className="live-dot" />API CONNECTED</div>
          <div className="user-card"><div className="avatar">{user.username?.slice(0, 1).toUpperCase()}</div><div className="user-details"><b>{user.username}</b><small>{String(user.role).replaceAll("_", " ")}</small></div><button title="Sign out" className="icon-button" onClick={signOut}>↗</button></div>
        </div>
      </aside>
      <main className="main">
        <header className="topbar">
          <div><div className="breadcrumb">SOC WORKSPACE <span>/</span> {title.toUpperCase()}</div><h1>{title}</h1></div>
          <div className="top-actions">
            <div className="search"><span>⌕</span><input placeholder="Search this view…" value={query} onChange={(e) => setQuery(e.target.value)} /><kbd>⌘ K</kbd></div>
            <button className="icon-button refresh" onClick={refresh} title="Refresh">↻</button>
            <div className="live-state"><i /> LIVE</div>
          </div>
        </header>
        {error && <div className="error-banner">{error}<button onClick={() => setError("")}>×</button></div>}
        {notice && <div className="notice-banner">{notice}<button onClick={() => setNotice("")}>×</button></div>}
        <div className="content">
          {selectedCaseId && selectedCase ? (
            <CaseDetail item={selectedCase} timeline={timeline} user={user} onBack={() => { setSelectedCaseId(null); setSelectedCase(null); }} onRefresh={reloadSelectedCase} notify={setNotice} />
          ) : page === "overview" ? (
            <Dashboard cases={visibleCases} alerts={visibleAlerts} events={visibleEvents} busy={busy} onOpenCase={openCase} onPage={setPage} />
          ) : page === "cases" ? (
            <CasesPage cases={visibleCases} busy={busy} onOpenCase={openCase} />
          ) : page === "alerts" ? (
            <AlertsPage alerts={visibleAlerts} busy={busy} user={user} onRefresh={refresh} notify={setNotice} />
          ) : (
            <EventsPage events={visibleEvents} busy={busy} />
          )}
          <footer className="footer"><span>SECURITY OPERATIONS CENTER</span><span>API <b>HEALTHY</b> · PostgreSQL</span></footer>
        </div>
      </main>
    </div>
  );
}

function Dashboard({ cases, alerts, events, busy, onOpenCase, onPage }) {
  const critical = alerts.filter((item) => String(item.severity).toLowerCase() === "critical" && item.status !== "CLOSED").length;
  const activeCases = cases.filter((item) => !["RESOLVED", "CLOSED"].includes(item.status)).length;
  return (
    <div className="page-stack">
      <section className="welcome-row"><div><p className="eyebrow">OPERATIONS SNAPSHOT</p><h2>Good to see you, analyst.</h2><p className="muted">A live view of current activity across your SOC.</p></div><div className="updated"><span className="live-dot" /> LIVE DATA</div></section>
      <section className="metric-grid">
        <Metric label="Open alerts" value={alerts.filter((item) => item.status !== "CLOSED").length} hint="Latest 100 alerts" icon="◈" tone="amber" />
        <Metric label="Critical alerts" value={critical} hint="Needs immediate attention" icon="⚠" tone="red" />
        <Metric label="Active cases" value={activeCases} hint="Latest 100 cases" icon="▣" tone="blue" />
        <Metric label="Events ingested" value={events.length} hint="Latest 100 events" icon="⌁" tone="green" />
      </section>
      <div className="dashboard-grid">
        <section className="panel span-two">
          <div className="panel-heading"><div><p className="eyebrow">PRIORITY QUEUE</p><h3>Recent alerts</h3></div><button className="text-button" onClick={() => onPage("alerts")}>View all →</button></div>
          <AlertTable alerts={alerts.slice(0, 6)} compact />
          {!alerts.length && <Empty text={busy ? "Loading alerts…" : "No alerts have been generated yet."} />}
        </section>
        <section className="panel">
          <div className="panel-heading"><div><p className="eyebrow">INVESTIGATIONS</p><h3>Recent cases</h3></div><button className="text-button" onClick={() => onPage("cases")}>View all →</button></div>
          <div className="mini-list">{cases.slice(0, 5).map((item) => <button className="mini-row" key={item.id} onClick={() => onOpenCase(item.id)}><span className="case-dot" /><span className="mini-title">{item.title}</span><b className={statusClass(item.priority)}>{item.priority}</b></button>)}</div>
          {!cases.length && <Empty text="No cases are available." />}
        </section>
        <section className="panel">
          <div className="panel-heading"><div><p className="eyebrow">TELEMETRY</p><h3>Recent events</h3></div><button className="text-button" onClick={() => onPage("events")}>View all →</button></div>
          <div className="event-feed">{events.slice(0, 5).map((item) => <div className="feed-row" key={item.id}><span className="feed-time">{date(item.timestamp)}</span><b>{item.event_type}</b><span>{item.hostname || item.log_source}</span></div>)}</div>
          {!events.length && <Empty text="No events ingested yet." />}
        </section>
      </div>
    </div>
  );
}

function Metric({ label, value, hint, icon, tone }) {
  return <article className="metric-card"><div className={"metric-icon " + tone}>{icon}</div><div className="metric-label">{label}</div><div className="metric-value">{value}</div><div className="metric-hint">{hint}</div><div className={"metric-accent " + tone} /></article>;
}

function CasesPage({ cases, busy, onOpenCase }) {
  const [status, setStatus] = useState("ALL");
  const rows = cases.filter((item) => status === "ALL" || item.status === status);
  return (
    <section className="panel">
      <div className="panel-heading"><div><p className="eyebrow">CASE MANAGEMENT</p><h3>Investigation queue <span className="count-chip">{rows.length}</span></h3></div><select value={status} onChange={(e) => setStatus(e.target.value)}><option value="ALL">All statuses</option>{["NEW", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CLOSED"].map((s) => <option key={s}>{s}</option>)}</select></div>
      {rows.length ? <div className="table-wrap"><table><thead><tr><th>CASE</th><th>PRIORITY</th><th>STATUS</th><th>ASSIGNED TO</th><th>CREATED</th><th /></tr></thead><tbody>{rows.map((item) => <tr key={item.id} onClick={() => onOpenCase(item.id)} className="click-row"><td><b>{item.title}</b><small className="subline">{String(item.id).slice(0, 8)}</small></td><td><span className={statusClass(item.priority)}>{item.priority}</span></td><td><span className={statusClass(item.status)}>{String(item.status).replaceAll("_", " ")}</span></td><td>{item.assigned_to || "Unassigned"}</td><td>{date(item.created_at)}</td><td className="arrow">→</td></tr>)}</tbody></table></div> : <Empty text={busy ? "Loading cases…" : "No cases match this view."} />}
    </section>
  );
}

function AlertsPage({ alerts, busy, user, onRefresh, notify }) {
  const [status, setStatus] = useState("ALL");
  const [severity, setSeverity] = useState("ALL");
  const rows = alerts.filter((item) => (status === "ALL" || item.status === status) && (severity === "ALL" || String(item.severity).toLowerCase() === severity));
  async function action(item, next) {
    try {
      await api.alertAction(item.id, next, next === "acknowledge" ? { analyst: user.username } : undefined);
      notify("Alert updated.");
      await onRefresh();
    } catch (err) {
      notify(err.message || "Could not update alert.");
    }
  }
  return (
    <section className="panel">
      <div className="panel-heading"><div><p className="eyebrow">TRIAGE AND RESPONSE</p><h3>Alert queue <span className="count-chip">{rows.length}</span></h3></div><div className="filters"><select value={status} onChange={(e) => setStatus(e.target.value)}><option value="ALL">All statuses</option>{["NEW", "ACKNOWLEDGED", "IN_PROGRESS", "CLOSED"].map((s) => <option key={s}>{s}</option>)}</select><select value={severity} onChange={(e) => setSeverity(e.target.value)}><option value="ALL">All severities</option>{["critical", "high", "medium", "low"].map((s) => <option key={s}>{s}</option>)}</select></div></div>
      {rows.length ? <div className="table-wrap"><table><thead><tr><th>ALERT</th><th>SEVERITY</th><th>STATUS</th><th>CREATED</th><th>ACTION</th></tr></thead><tbody>{rows.map((item) => <tr key={item.id}><td><b>{item.title}</b><small className="subline">{String(item.id).slice(0, 8)}</small></td><td><span className={statusClass(item.severity)}>{String(item.severity).toUpperCase()}</span></td><td><span className={statusClass(item.status)}>{String(item.status).replaceAll("_", " ")}</span></td><td>{date(item.created_at)}</td><td>{item.status === "NEW" ? <button className="button small-button" onClick={() => action(item, "acknowledge")}>Acknowledge</button> : item.status === "ACKNOWLEDGED" ? <button className="button small-button" onClick={() => action(item, "start")}>Investigate</button> : <span className="muted">—</span>}</td></tr>)}</tbody></table></div> : <Empty text={busy ? "Loading alerts…" : "No alerts match these filters."} />}
    </section>
  );
}

function AlertTable({ alerts, compact = false }) {
  if (!alerts.length) return null;
  return <div className="table-wrap"><table><thead><tr><th>ALERT</th><th>SEVERITY</th><th>STATUS</th><th>CREATED</th></tr></thead><tbody>{alerts.map((item) => <tr key={item.id}><td><b>{item.title}</b>{!compact && <small className="subline">{String(item.id).slice(0, 8)}</small>}</td><td><span className={statusClass(item.severity)}>{String(item.severity).toUpperCase()}</span></td><td><span className={statusClass(item.status)}>{item.status}</span></td><td>{date(item.created_at)}</td></tr>)}</tbody></table></div>;
}

function EventsPage({ events, busy }) {
  const [kind, setKind] = useState("ALL");
  const types = [...new Set(events.map((item) => item.event_type).filter(Boolean))].sort();
  const rows = events.filter((item) => kind === "ALL" || item.event_type === kind);
  return (
    <section className="panel">
      <div className="panel-heading"><div><p className="eyebrow">INGESTION STREAM</p><h3>Security events <span className="count-chip">{rows.length}</span></h3></div><select value={kind} onChange={(e) => setKind(e.target.value)}><option value="ALL">All event types</option>{types.map((type) => <option key={type}>{type}</option>)}</select></div>
      {rows.length ? <div className="table-wrap"><table><thead><tr><th>TIMESTAMP</th><th>EVENT TYPE</th><th>HOST / SOURCE</th><th>USER</th><th>MESSAGE</th></tr></thead><tbody>{rows.map((item) => <tr key={item.id}><td>{date(item.timestamp)}</td><td><span className="event-type">{item.event_type}</span></td><td><b>{item.hostname || "—"}</b><small className="subline">{item.log_source}</small></td><td>{item.username || "—"}</td><td className="message-cell">{item.message}</td></tr>)}</tbody></table></div> : <Empty text={busy ? "Loading events…" : "No events ingested yet."} />}
    </section>
  );
}

function CaseDetail({ item, timeline, user, onBack, onRefresh, notify }) {
  const [comment, setComment] = useState("");
  const [evidence, setEvidence] = useState({ name: "", description: "", source: "" });
  const [team, setTeam] = useState("Tier 1 SOC");
  const [reason, setReason] = useState("");
  const [summary, setSummary] = useState("");
  const [saving, setSaving] = useState(false);

  async function act(action, body) {
    setSaving(true);
    try {
      await api.caseAction(item.id, action, body);
      notify("Case updated.");
      await onRefresh();
    } catch (err) {
      notify(err.message || "Could not update case.");
    } finally {
      setSaving(false);
    }
  }

  async function sendComment(event) {
    event.preventDefault();
    if (!comment.trim()) return;
    setSaving(true);
    try {
      await api.addComment(item.id, { author: user.username, message: comment });
      setComment("");
      await onRefresh();
      notify("Comment added to the investigation.");
    } catch (err) {
      notify(err.message || "Could not add comment.");
    } finally {
      setSaving(false);
    }
  }

  async function sendEvidence(event) {
    event.preventDefault();
    setSaving(true);
    try {
      await api.addEvidence(item.id, evidence);
      setEvidence({ name: "", description: "", source: "" });
      await onRefresh();
      notify("Evidence added to the investigation.");
    } catch (err) {
      notify(err.message || "Could not add evidence.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="page-stack">
      <button className="back-link" onClick={onBack}>← Back to cases</button>
      <section className="case-hero panel">
        <div className="case-title-row"><div><p className="eyebrow">CASE {String(item.id).slice(0, 8).toUpperCase()}</p><h2>{item.title}</h2><p className="muted">Created {date(item.created_at)} · {item.assigned_to || "Unassigned"}</p></div><div className="case-badges"><span className={statusClass(item.priority)}>{item.priority}</span><span className={statusClass(item.status)}>{String(item.status).replaceAll("_", " ")}</span></div></div>
        <div className="action-row">
          {item.status === "NEW" && <form className="inline-form" onSubmit={(e) => { e.preventDefault(); act("assign", { team, assigned_by: user.username, reason: reason || "Assigned from SOC console" }); }}><input aria-label="Team" value={team} onChange={(e) => setTeam(e.target.value)} /><input aria-label="Assignment reason" placeholder="Assignment reason" value={reason} onChange={(e) => setReason(e.target.value)} /><button className="button primary small-button" disabled={saving}>Assign</button></form>}
          {item.status === "ASSIGNED" && <button className="button primary" disabled={saving} onClick={() => act("start", { analyst: user.username })}>Start investigation</button>}
          {item.status === "IN_PROGRESS" && <><select aria-label="Change priority" value={item.priority} onChange={(e) => act("priority", { priority: e.target.value, changed_by: user.username })}>{["LOW", "MEDIUM", "HIGH", "CRITICAL"].map((p) => <option key={p}>{p}</option>)}</select><form className="inline-form" onSubmit={(e) => { e.preventDefault(); act("resolve", { resolution_type: "ANALYST_RESOLVED", summary, resolved_by: user.username }); }}><input placeholder="Resolution summary" value={summary} onChange={(e) => setSummary(e.target.value)} required /><button className="button primary small-button" disabled={saving}>Resolve</button></form></>}
          {item.status === "RESOLVED" && roleCanManage(user.role) && <button className="button primary" disabled={saving} onClick={() => act("close", { closed_by: user.username })}>Close case</button>}
        </div>
      </section>
      <div className="detail-grid">
        <section className="panel timeline-panel"><div className="panel-heading"><div><p className="eyebrow">AUDIT TRAIL</p><h3>Investigation timeline</h3></div><span className="count-chip">{timeline.length} entries</span></div>
          {timeline.length ? <div className="timeline">{timeline.map((event) => <div className="timeline-item" key={event.event_id}><span className="timeline-node" /><div><div className="timeline-heading"><b>{String(event.event_type).replaceAll("_", " ")}</b><time>{date(event.occurred_at)}</time></div><p>{event.description}</p>{event.actor && <small>BY {event.actor}</small>}</div></div>)}</div> : <Empty text="No timeline entries." />}
        </section>
        <section className="panel"><div className="panel-heading"><div><p className="eyebrow">ANALYST NOTES</p><h3>Comments</h3></div></div>
          <form className="stack compact-stack" onSubmit={sendComment}><textarea placeholder="Add an investigation note…" value={comment} onChange={(e) => setComment(e.target.value)} required /><button className="button primary" disabled={saving}>Add comment</button></form>
          <div className="record-list">{(item.comments || []).slice().reverse().map((entry, index) => <article className="record" key={index}><div className="record-meta"><b>{entry.author}</b><time>{date(entry.created_at)}</time></div><p>{entry.message}</p></article>)}</div>
        </section>
      </div>
      <section className="panel"><div className="panel-heading"><div><p className="eyebrow">COLLECTED ARTIFACTS</p><h3>Evidence</h3></div></div>
        <form className="evidence-form" onSubmit={sendEvidence}><input placeholder="Evidence name" value={evidence.name} onChange={(e) => setEvidence({ ...evidence, name: e.target.value })} required /><input placeholder="Source (event ID, IP, URL…)" value={evidence.source} onChange={(e) => setEvidence({ ...evidence, source: e.target.value })} required /><input placeholder="Description" value={evidence.description} onChange={(e) => setEvidence({ ...evidence, description: e.target.value })} required /><button className="button primary" disabled={saving}>Add evidence</button></form>
        {(item.evidence || []).length ? <div className="evidence-list">{item.evidence.map((entry, index) => <div className="evidence-card" key={index}><b>{entry.name}</b><span>{entry.source}</span><p>{entry.description}</p></div>)}</div> : <Empty text="No evidence attached yet." />}
      </section>
    </div>
  );
}

function Empty({ text }) {
  return <div className="empty-state"><span>◇</span><p>{text}</p></div>;
}

function main() {
  createRoot(document.getElementById("root")).render(<App />);
}

main();


(() => {
  "use strict";

  const byId = (id) => document.getElementById(id);
  const editor = byId("editor");
  const keyboard = byId("keyboard");
  const details = byId("key-details");
  const status = byId("status");
  const statusLabel = byId("status-label");
  const errorHelp = byId("error-help");
  const errorDetail = byId("error-detail");
  const feedback = byId("feedback");
  const copyButton = byId("copy");
  const clearButton = byId("clear");
  const inspectButton = byId("inspect");
  const unicodePanel = byId("unicode-panel");
  const codepoints = byId("codepoints");
  const count = byId("count");
  const keystrokeLog = byId("keystroke-log");
  const keystrokePlaceholder = byId("keystroke-placeholder");
  const clearKeystrokesButton = byId("clear-keystrokes");
  const themeControl = byId("theme");
  const geometryControl = byId("geometry");
  const layerHint = byId("layer-hint");
  const modifierIndicator = byId("modifier-indicator");
  const layerButtons = [...document.querySelectorAll("[data-layer]")];

  const layerNames = ["Base", "Shift", "AltGr", "Shift + AltGr"];
  const backtick = String.fromCharCode(96);
  const keyCodes = {
    [backtick]: "Backquote", "-": "Minus", "=": "Equal",
    "[": "BracketLeft", "]": "BracketRight", "\\": "Backslash",
    ";": "Semicolon", "'": "Quote", ",": "Comma",
    ".": "Period", "/": "Slash", "§": "IntlBackslash", " ": "Space"
  };
  const physicalCode = (key) => {
    if (/^[A-Z]$/.test(key)) return "Key" + key;
    if (/^[0-9]$/.test(key)) return "Digit" + key;
    return keyCodes[key];
  };
  const rowsFor = () => {
    const iso = geometryControl.value === "iso";
    return [
      backtick + "1234567890-=",
      "QWERTYUIOP[]" + (iso ? "" : "\\"),
      "ASDFGHJKL;'" + (iso ? "\\" : ""),
      (iso ? "§" : "") + "ZXCVBNM,./",
      " "
    ];
  };

  let mapping = null;
  let keymanReady = false;
  let layoutError = null;
  let typingError = null;
  let selectedLayer = 0;
  let pointerKey = null;
  let renderedGeometry = null;
  let shiftDown = false;
  let altGrDown = false;
  const heldKeys = new Set();

  // The keymap only visualizes characters. KeymanWeb owns actual typing.
  function readable(value) {
    if (value === null || value === undefined) return "—";
    if (value === "\u200d") return "ZWJ";
    if (value === "\u200c") return "ZWNJ";
    if (value === " ") return "Space";
    if (/^\p{Mark}$/u.test(value)) return "◌" + value;
    return value;
  }

  function activeLayer() {
    return shiftDown || altGrDown
      ? Number(shiftDown) + Number(altGrDown) * 2
      : selectedLayer;
  }

  // The visual reference and Keyman input load independently. One failing
  // should never hide the other when it is working.
  function displayError(source, message) {
    if (source === "layout") layoutError = String(message);
    else typingError = String(message);
    displayStatus();
  }

  function displayStatus() {
    const problems = [];
    if (layoutError) problems.push("Keyboard reference: " + layoutError);
    if (typingError) problems.push("Typing: " + typingError);
    const hasError = problems.length > 0;

    status.classList.toggle("error", hasError);
    status.classList.toggle("ready", !hasError && !!mapping && keymanReady);
    errorHelp.hidden = !hasError;
    errorDetail.textContent = problems.join(" · ");

    if (typingError) {
      statusLabel.textContent = "Typing unavailable";
    } else if (layoutError) {
      statusLabel.textContent = keymanReady
        ? "Typing ready · Reference unavailable"
        : "Reference unavailable · Connecting keyboard…";
    } else if (mapping && keymanReady) {
      statusLabel.textContent = "Onnoy ready";
    } else if (mapping) {
      statusLabel.textContent = "Keyboard reference ready · Connecting…";
    } else if (keymanReady) {
      statusLabel.textContent = "Typing ready · Loading reference…";
    } else {
      statusLabel.textContent = "Connecting keyboard…";
    }
  }

  // Highlight only while a physical key or pointer is actually held.
  function syncHighlights() {
    for (const button of keyboard.querySelectorAll(".keyboard-key")) {
      const held = heldKeys.has(button.dataset.code) || button.dataset.key === pointerKey;
      button.classList.toggle("pressed", held);
      button.setAttribute("aria-pressed", String(held));
    }
  }

  function showDetails(key) {
    if (!mapping || !key) return;
    const values = mapping[physicalCode(key)];
    if (!values) return;

    const heading = document.createElement("strong");
    heading.className = "inspector-key";
    heading.textContent = key === " " ? "Space" : key === "§" ? "ISO extra key" : key;

    const grid = document.createElement("div");
    grid.className = "inspector-outputs";
    values.forEach((value, index) => {
      const cell = document.createElement("div");
      cell.className = "inspector-output";
      const label = document.createElement("span");
      label.className = "inspector-layer";
      label.textContent = layerNames[index];
      const glyph = document.createElement("strong");
      glyph.textContent = readable(value);
      glyph.lang = value === "\u200c" || value === "\u200d" ? "en" : "bn";
      cell.append(label, glyph);
      grid.append(cell);
    });
    details.replaceChildren(heading, grid);
  }

  function drawKeyboard() {
    if (!mapping) return;
    const layer = activeLayer();
    layerHint.textContent = shiftDown || altGrDown
      ? "Physical modifier held · Visual layer updates as you type"
      : "Select a layer above or hold Shift / Right Alt to preview";
    modifierIndicator.textContent = layerNames[layer].toUpperCase();
    for (const button of layerButtons) {
      const active = Number(button.dataset.layer) === layer;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    }

    // Key geometry rarely changes. Keep the DOM and pointer handlers stable
    // when Shift/AltGr changes; update the characters in place instead.
    if (renderedGeometry !== geometryControl.value) {
      const fragment = document.createDocumentFragment();
      for (const rowKeys of rowsFor()) {
        const row = document.createElement("div");
        row.className = "keyboard-row";
        for (const key of rowKeys) {
          const button = document.createElement("button");
          button.type = "button";
          button.className = "keyboard-key";
          button.dataset.key = key;
          button.dataset.code = physicalCode(key);
          const glyph = document.createElement("span");
          glyph.className = "key-output";
          const caption = document.createElement("span");
          caption.className = "key-label";
          caption.textContent = key === " " ? "SPACE" : key === "§" ? "ISO" : key;
          button.append(glyph, caption);
          row.append(button);
        }
        fragment.append(row);
      }
      keyboard.replaceChildren(fragment);
      renderedGeometry = geometryControl.value;
    }

    for (const button of keyboard.querySelectorAll(".keyboard-key")) {
      const key = button.dataset.key;
      const value = mapping[button.dataset.code][layer];
      const glyph = button.querySelector(".key-output");
      glyph.textContent = readable(value);
      const joiner = value === "\u200c" || value === "\u200d";
      glyph.classList.toggle("key-joiner", joiner);
      glyph.lang = joiner ? "en" : "bn";
      button.classList.toggle("unassigned", value === null);
      button.setAttribute("aria-label",
        (key === "§" ? "ISO extra key" : key === " " ? "Space" : key) +
        ", " + layerNames[layer] + ": " + readable(value));
    }
    syncHighlights();
  }

  keyboard.addEventListener("pointerdown", (event) => {
    const button = event.target.closest(".keyboard-key");
    if (!button || event.button !== 0) return;
    pointerKey = button.dataset.key;
    syncHighlights();
    showDetails(pointerKey);
  });
  keyboard.addEventListener("click", (event) => {
    const button = event.target.closest(".keyboard-key");
    if (button) showDetails(button.dataset.key);
  });

  for (const button of layerButtons) {
    button.addEventListener("click", () => {
      selectedLayer = Number(button.dataset.layer);
      // An explicit preview selection always wins, even after an OS has
      // swallowed a modifier keyup while the editor was focused.
      shiftDown = false;
      altGrDown = false;
      drawKeyboard();
    });
  }

  geometryControl.addEventListener("change", () => {
    pointerKey = null;
    heldKeys.clear();
    renderedGeometry = null;
    drawKeyboard();
    details.textContent = "Select a key to inspect all four outputs.";
  });

  function modifierState(event, down) {
    const wasShift = shiftDown;
    const wasAltGr = altGrDown;
    const graph = typeof event.getModifierState === "function" &&
      event.getModifierState("AltGraph");
    if (event.key === "Shift" || event.code === "ShiftLeft" || event.code === "ShiftRight") {
      shiftDown = down;
    } else {
      shiftDown = !!event.shiftKey;
    }
    if (event.code === "AltRight" || event.key === "AltGraph") {
      altGrDown = down;
    } else {
      altGrDown = !!graph || (altGrDown && event.altKey);
    }
    if (shiftDown !== wasShift || altGrDown !== wasAltGr) drawKeyboard();
  }

  // Record only physical keys pressed in the writing area, not text content.
  // Shortcuts, modifier-only presses, paste and other controls are ignored.
  const MAX_KEYSTROKES = 100;

  function clearKeystrokes() {
    keystrokeLog.replaceChildren(keystrokePlaceholder);
    keystrokePlaceholder.hidden = false;
    clearKeystrokesButton.disabled = true;
  }

  function removeLastKeystroke() {
    keystrokeLog.querySelector(".keystroke-token:last-child")?.remove();
    const empty = !keystrokeLog.querySelector(".keystroke-token");
    keystrokePlaceholder.hidden = !empty;
    clearKeystrokesButton.disabled = empty;
  }

  function recordKeystroke(event, key) {
    if (event.target !== editor || event.isComposing || event.metaKey) return;

    const altGr = altGrDown ||
      (typeof event.getModifierState === "function" && event.getModifierState("AltGraph")) ||
      (event.ctrlKey && event.altKey);
    if ((event.ctrlKey || event.altKey) && !altGr) return;

    // Backspace edits the history; it is not a recorded keystroke.
    if (event.code === "Backspace") {
      if (!event.ctrlKey && !event.altKey) removeLastKeystroke();
      return;
    }

    let label;
    let name;
    if (event.code === "Enter") {
      label = "↵";
      name = "Enter";
    } else if (key) {
      const letter = /^[A-Z]$/.test(key);
      const base = key === " " ? "␣" : key === "§" ? "ISO" :
        letter ? (event.shiftKey ? key : key.toLowerCase()) : key;
      label = (altGr ? "⇮" : "") +
        (event.shiftKey && !letter ? "⇧" : "") + base;
      name = (altGr ? "AltGr + " : "") +
        (event.shiftKey ? "Shift + " : "") +
        (key === " " ? "Space" : key === "§" ? "ISO extra key" : key);
    } else {
      return;
    }

    keystrokePlaceholder.hidden = true;
    const token = document.createElement("kbd");
    token.className = "keystroke-token";
    if (altGr) token.classList.add("keystroke-altgr");
    token.textContent = label;
    token.setAttribute("aria-label", name);
    token.title = name;
    keystrokeLog.append(token);
    while (keystrokeLog.children.length > MAX_KEYSTROKES + 1) {
      keystrokeLog.children[1].remove();
    }
    clearKeystrokesButton.disabled = false;
    keystrokeLog.scrollTop = keystrokeLog.scrollHeight;
  }

  clearKeystrokesButton.addEventListener("click", clearKeystrokes);

  // Capture before KeymanWeb handles the focused editor. Physical codes,
  // unlike event.key, are stable across Shift, AltGr and keyboard layouts.
  function trackKey(event, down) {
    modifierState(event, down);
    const key = [...rowsFor().join("")].find((label) => physicalCode(label) === event.code);
    if (down) recordKeystroke(event, key);
    if (!key || !mapping) return;
    if (down) {
      heldKeys.add(event.code);
      showDetails(key);
    } else {
      heldKeys.delete(event.code);
    }
    syncHighlights();
  }

  window.addEventListener("pointerup", () => {
    pointerKey = null;
    syncHighlights();
  }, true);
  window.addEventListener("pointercancel", () => {
    pointerKey = null;
    syncHighlights();
  }, true);
  window.addEventListener("keydown", (event) => trackKey(event, true), true);
  window.addEventListener("keyup", (event) => trackKey(event, false), true);
  window.addEventListener("blur", () => {
    shiftDown = false;
    altGrDown = false;
    heldKeys.clear();
    pointerKey = null;
    drawKeyboard();
  });

  // System is the default. Explicit theme choices persist across visits.
  const themeValues = new Set(["system", "light", "dark"]);
  function applyTheme(value) {
    const chosen = themeValues.has(value) ? value : "system";
    themeControl.value = chosen;
    if (chosen === "system") {
      document.documentElement.removeAttribute("data-theme");
    } else {
      document.documentElement.dataset.theme = chosen;
    }
    const prefersDark = window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;
    const dark = chosen === "dark" || (chosen === "system" && prefersDark);
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = dark ? "#171d1b" : "#f7f6f2";
  }
  let savedTheme = "system";
  try {
    savedTheme = window.localStorage.getItem("onnoy-theme") || "system";
  } catch {
    // Private browsing can disable localStorage; System still works.
  }
  applyTheme(savedTheme);
  themeControl.addEventListener("change", () => {
    applyTheme(themeControl.value);
    try {
      if (themeControl.value === "system") {
        window.localStorage.removeItem("onnoy-theme");
      } else {
        window.localStorage.setItem("onnoy-theme", themeControl.value);
      }
    } catch { /* preference applies to this visit */ }
  });
  if (window.matchMedia) {
    const media = window.matchMedia("(prefers-color-scheme: dark)");
    if (media.addEventListener) {
      media.addEventListener("change", () => {
        if (themeControl.value === "system") applyTheme("system");
      });
    }
  }

  const segmenter = typeof Intl.Segmenter === "function"
    ? new Intl.Segmenter("bn", { granularity: "grapheme" }) : null;
  function updateEditor() {
    const chars = [...editor.value];
    const graphemes = segmenter ? [...segmenter.segment(editor.value)].length : chars.length;
    count.textContent = chars.length + " code points · " + graphemes + " graphemes";
    copyButton.disabled = chars.length === 0;
    if (!unicodePanel.hidden) {
      codepoints.replaceChildren();
      if (!chars.length) {
        codepoints.textContent = "Nothing to inspect yet.";
      } else {
        for (const char of chars) {
          const part = document.createElement("span");
          part.textContent = readable(char) + " U+" +
            char.codePointAt(0).toString(16).toUpperCase().padStart(4, "0");
          codepoints.append(part);
        }
      }
    }
  }
  editor.addEventListener("input", () => {
    feedback.textContent = "";
    updateEditor();
  });
  inspectButton.addEventListener("click", () => {
    unicodePanel.hidden = !unicodePanel.hidden;
    inspectButton.setAttribute("aria-expanded", String(!unicodePanel.hidden));
    updateEditor();
  });
  clearButton.addEventListener("click", () => {
    editor.value = "";
    feedback.textContent = "";
    clearKeystrokes();
    updateEditor();
    editor.focus();
  });
  copyButton.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(editor.value);
      feedback.textContent = "Copied!";
    } catch {
      editor.focus();
      editor.select();
      feedback.textContent = "Clipboard unavailable — text selected. Press Ctrl+C or ⌘C.";
    }
  });
  for (const button of document.querySelectorAll("[data-sample]")) {
    button.addEventListener("click", () => {
      editor.value = button.dataset.sample || "";
      clearKeystrokes();
      feedback.textContent = "Example inserted";
      updateEditor();
      editor.focus();
    });
  }
  updateEditor();

  async function loadLayout() {
    try {
      const response = await fetch("./layout.json");
      if (!response.ok) throw new Error("Unable to fetch generated keymap (HTTP " + response.status + ")");
      const layout = await response.json();
      // Verify the complete ANSI and ISO set, not only the initially chosen
      // geometry; sparse modifier slots must stay explicitly null.
      const codes = new Set([...rowsFor().join("")].map(physicalCode));
      codes.add("IntlBackslash");
      if (!layout.keys || [...codes].some((code) => {
        const values = layout.keys[code];
        return !Array.isArray(values) || values.length !== 4 ||
          values.some((value) => value !== null && (typeof value !== "string" || [...value].length !== 1));
      })) {
        throw new Error("Invalid four-layer keymap");
      }
      mapping = layout.keys;
      drawKeyboard();
      displayStatus();
    } catch (error) {
      keyboard.textContent = "Could not load the Onnoy keyboard reference.";
      displayError("layout", error.message || error);
    }
  }

  async function startKeyman() {
    try {
      const engine = window.keyman;
      if (!engine || typeof engine.init !== "function") {
        throw new Error("KeymanWeb failed to load");
      }
      await engine.init({ attachType: "auto" });
      await engine.addKeyboards({
        id: "onnoy",
        name: "Onnoy",
        language: { id: "bn", name: "Bengali" },
        filename: "./onnoy.js"
      });
      await engine.setActiveKeyboard("onnoy", "bn");
      // Desktop already has our own visual keyboard. Disable KeymanWeb's
      // separate floating OSK so it cannot cover the editor or page.
      // Keep the touch OSK available on phones and tablets.
      if (window.matchMedia("(hover: hover) and (pointer: fine)").matches &&
          engine.osk && typeof engine.osk.hide === "function") {
        engine.osk.hide();
      }
      keymanReady = true;
      displayStatus();
    } catch (error) {
      displayError("typing", error.message || error);
    }
  }

  void loadLayout();
  // The app script runs before KeymanWeb so capture listeners are installed
  // first. Initialize the engine after both deferred scripts have loaded.
  window.addEventListener("load", () => { void startKeyman(); }, { once: true });
})();

"use strict";

// Kalamine is the diagram source. Only KeymanWeb inserts text.
const keyboard = document.querySelector("x-keyboard");
const editor = document.querySelector("#editor");
const status = document.querySelector("#status");

async function loadDiagram() {
  try {
    // Do not block KeymanWeb when the optional diagram cannot load.
    await customElements.whenDefined("x-keyboard");
    const response = await fetch("./onnoy.json");
    if (!response.ok) throw new Error("could not fetch diagram data");
    const layout = await response.json();
    keyboard.setKeyboardLayout(layout.keymap, layout.deadkeys, layout.geometry);
    document.querySelector("#geometry").addEventListener("change", event => {
      keyboard.geometry = event.target.value;
    });
    // Highlight keys, but discard the component's emulated text output.
    editor.addEventListener("keydown", event => { keyboard.keyDown(event); }, true);
    editor.addEventListener("keyup", event => { keyboard.keyUp(event); }, true);
    editor.addEventListener("blur", () => keyboard.clearStyle());
  } catch (error) {
    document.querySelector("#map-status").textContent =
      "Keyboard diagram unavailable: " + error.message;
  }
}

async function startTyping() {
  try {
    if (!window.keyman) throw new Error("KeymanWeb did not load");
    await window.keyman.init({attachType: "auto"});
    await window.keyman.addKeyboards({
      id: "onnoy",
      name: "Onnoy",
      language: {id: "bn", name: "Bangla"},
      filename: "./onnoy.js"
    });
    await window.keyman.setActiveKeyboard("onnoy", "bn");
    if (matchMedia("(hover: hover) and (pointer: fine)").matches) {
      window.keyman.osk?.hide();
    }
    status.textContent = "Ready — Onnoy typing enabled";
  } catch (error) {
    status.textContent = "Typing unavailable: " + error.message;
  }
}

document.querySelector("#clear").addEventListener("click", () => {
  editor.value = "";
  editor.focus();
});
document.querySelector("#copy").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(editor.value);
    status.textContent = "Copied";
  } catch {
    editor.select();
    status.textContent = "Select and copy the text";
  }
});

window.addEventListener("load", () => {
  void loadDiagram();
  void startTyping();
});

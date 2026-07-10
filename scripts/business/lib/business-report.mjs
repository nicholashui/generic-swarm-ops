export function createReport(title) {
  return {
    title,
    sections: [],
    addSection(name, items = []) {
      this.sections.push({ name, items: [...items] });
    }
  };
}

export function reportToText(report) {
  const lines = [`# ${report.title}`];
  for (const section of report.sections) {
    lines.push("");
    lines.push(`## ${section.name}`);
    if (section.items.length === 0) {
      lines.push("");
      lines.push("- none");
      continue;
    }
    lines.push("");
    for (const item of section.items) {
      lines.push(`- ${item}`);
    }
  }
  return `${lines.join("\n")}\n`;
}

export function printReport(report) {
  process.stdout.write(reportToText(report));
}

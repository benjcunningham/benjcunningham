import logging
import os
import subprocess

import pandas as pd
from jinja2 import Template
from omegaconf import OmegaConf


log = logging.getLogger(__name__)
ci_dir = os.path.dirname(os.path.abspath(__file__))


def render_readme(outdir, **kwargs):

    template_path = os.path.join(ci_dir, "template.md")

    with open(template_path, "r") as file:
        template = Template(file.read())

    readme_str = template.render(**kwargs)

    with open(os.path.join(outdir, "README.md"), "w") as file:
        file.write(readme_str)


def status_badge(proj):

    if not proj.get("badges"):
        return None

    badges = []

    for workflow in proj.badges:

        ci_link = "https://github.com/{}/actions/workflows/{}".format(
            proj.repo, workflow
        )
        img_link = "{}/badge.svg".format(ci_link)

        badges.append("[![{}]({})]({})".format(workflow, img_link, ci_link))

    badge = " <br> ".join(badges)

    return badge


def project_link(proj):

    value = proj.name

    if proj.get("repo"):
        value = "[{}](https://github.com/{})".format(value, proj.repo)

    return value


def current_release(proj):

    if not proj.get("repo"):
        log.warning("Skipping release: no repository information")
        return None

    url = "https://github.com/{}".format(proj.repo)
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tags.sh")
    res = subprocess.run(
        script_path,
        env={**dict(os.environ), "URL": url},
        capture_output=True,
    )

    tags = res.stdout.decode()

    if not tags:
        if res.stderr:
            log.error("Failed fetching releases: %s", res.stderr.decode())
        else:
            log.warning("Repository has no releases")
        return None

    tag_name = tags.split()[-1].split("refs/tags/")[-1]
    release_url = "{}/releases/tag/{}".format(url, tag_name)
    release_link = "[{}]({})".format(tag_name, release_url)

    return release_link


def create_table(projects):

    data = []

    for proj in projects:

        log.info("Processing `%s`", proj.name)

        data.append(
            {
                "Name": project_link(proj),
                "Status": status_badge(proj),
                "Current Release": current_release(proj),
            }
        )

    table = pd.DataFrame(data)
    md = table.to_markdown(index=False)

    return md


def create_tables():

    conf_path = os.path.join(os.path.dirname(ci_dir), "dashboard.yaml")
    conf = OmegaConf.load(conf_path)

    tables = {key: create_table(projs) for key, projs in conf.items()}

    return tables


def main():

    tables = create_tables()

    render_readme(".", tables=tables)


if __name__ == "__main__":
    main()

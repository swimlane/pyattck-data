from .base import Base


class SplunkSecurityContent(Base):
    """
    Data Source: https://raw.githubusercontent.com/splunk/security_content/develop/dist/api/detections.json
    Authors:
        - Splunk

    This class is a wrapper for the above data set
    """
    URL = 'https://raw.githubusercontent.com/splunk/security_content/develop/dist/api/detections.json'

    def parse(self):
        self.count = 0
        self.actor_count = 0
        data = self.session.get(self.URL).json()
        for item in data.get("detections"):
            if item.get("tags"):
                if item["tags"].get("mitre_attack_enrichments"):
                    for enrichment in item["tags"]["mitre_attack_enrichments"]:
                        if enrichment.get("mitre_attack_id"):
                            tech = self.helper.get_object_by_external_id(enrichment["mitre_attack_id"], "attack-pattern")
                            tech.possible_detections.append({"name": item["name"], "description": item["description"], "search": item["search"], "tags": item["tags"]})
                            tech.external_references.extend(item.get("external_references",[]))
                            self.count += 1
                            self.helper.replace_object(tech)
                        if enrichment.get("mitre_attack_groups"):
                            for group in enrichment["mitre_attack_groups"]:
                                actor = self.helper.get_object_by_name_or_aliases(group, "intrusion-set")
                                actor.links.extend(item.get("external_references", []))
                                self.actor_count += 1
                                self.helper.replace_object(actor)
        self.__logger.info(f"Updated {self.count} techniques and {self.actor_count} actors")

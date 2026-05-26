CONTACT_MEMORY_TIME = 5.0


class AwarenessSystem:

    def __init__(self):

        self.contacts = {}

    # =====================================================
    # UPDATE CONTACT
    # =====================================================

    def update_contact(
        self,
        target,
        currently_visible,
        current_time
    ):

        target_id = id(target)

        # =================================================
        # TARGET VISIBLE
        # =================================================

        if currently_visible:

            self.contacts[target_id] = {

                "target": target,

                "visible": True,

                "last_seen_time": current_time,

                "last_known_x": target.x,
                "last_known_y": target.y
            }

            return

        # =================================================
        # TARGET NOT VISIBLE
        # =================================================

        if target_id in self.contacts:

            self.contacts[target_id]["visible"] = False

    # =====================================================
    # CLEANUP
    # =====================================================

    def cleanup_contacts(
        self,
        current_time
    ):

        expired = []

        for target_id, contact in self.contacts.items():

            age = (
                current_time -
                contact["last_seen_time"]
            )

            if age > CONTACT_MEMORY_TIME:

                expired.append(target_id)

        for target_id in expired:

            del self.contacts[target_id]

    # =====================================================
    # QUERY
    # =====================================================

    def knows_target(
        self,
        target
    ):

        return id(target) in self.contacts

    def target_visible(
        self,
        target
    ):

        target_id = id(target)

        if target_id not in self.contacts:
            return False

        return self.contacts[target_id]["visible"]

    def get_last_known_position(
        self,
        target
    ):

        target_id = id(target)

        if target_id not in self.contacts:
            return None

        contact = self.contacts[target_id]

        return (

            contact["last_known_x"],
            contact["last_known_y"]
        )
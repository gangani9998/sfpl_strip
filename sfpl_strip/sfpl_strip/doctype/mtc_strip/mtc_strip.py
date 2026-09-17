# Copyright (c) 2026, Jay Kumar Gangani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class MTCStrip(Document):
    def validate(self):
        self.calculate_means()

    def calculate_means(self):
        # 1. Calculate U Specimen Data (GeoStrap)
        total_ts_1 = 0.0
        total_ed = 0.0
        total_eu = 0.0
        count_1 = 0
        
        if self.specimen_data:
            for d in self.specimen_data:
                total_ts_1 += flt(d.tensile_strenth)
                total_ed += flt(d.elongation_at_designeted)
                total_eu += flt(d.elongation_at_ultimate)
                count_1 += 1
                
        if count_1 > 0:
            self.mean_tensile_strength = total_ts_1 / count_1
            self.mean_elongation_designated = total_ed / count_1
            self.mean_elongation_ultimate = total_eu / count_1
        else:
            self.mean_elongation_designated = 0.0
            self.mean_elongation_ultimate = 0.0

        # 2. Calculate System Strength Data (Packstrap)
        total_ss = 0.0
        count_2 = 0
        
        if hasattr(self, 'system_strength_data') and self.system_strength_data:
            for d in self.system_strength_data:
                total_ss += flt(d.system_strength)
                count_2 += 1
                
        if count_2 > 0:
            self.mean_system_strength = total_ss / count_2
        else:
            self.mean_system_strength = 0.0
            
        # If both empty
        if count_1 == 0 and count_2 == 0:
            self.mean_tensile_strength = 0.0

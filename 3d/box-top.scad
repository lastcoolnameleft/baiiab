
// LED Display Datasheets.  Technically from 52pi.com, but close enough to Adafruit, except for some dimensions
// https://wiki.52pi.com/index.php?title=Z-0235
// https://cdn-shop.adafruit.com/datasheets/TC2004A-01.pdf
// https://52pi.com/products/52pi-2004-serial-lcd-module-display

// TODO!  UPDATE BEFORE FINAL STL.  30 seems to be good; 5 renders fast
$fn = 30;
is_center = false;

render_delta = 0.1;

case_top_x = 155; // lid length
case_top_y = 105; // lid height
case_top_z = 5; // lid_thickness
case_top_inset = 5;
case_top_thickness = 3;

case_x = case_top_x; // same as case_top_x
case_y = case_top_y; // same as case_top_y
case_z = 95; // case height
case_thickness = case_top_inset; // thickness == how far we've inset the top walls

lcd_screen_x = 97.5;
lcd_screen_y = 40;
lcd_screen_z = 9.4;

pcb_x = 98.15;
pcb_y = 60;
pcb_z = 1.6;
    
screwhole_radius = 3 / 2; // 3mm diameter
screwhole_x = 93 / 2; // distance from center of lcd_screen to screwhole
screwhole_y = 55 / 2;
screwhole_z = lcd_screen_z - case_top_z;

button_radius = 7.5 / 2; // buttons are 24mm wide

printer_hole_translate_y = 46; // ((case_top_y - (lcd_screen_y + button_radius)) / 3)*2 + 5;
button_hole_translate_y = 23.5; // ((case_top_y - (lcd_screen_y + button_radius)) / 3) + 3;

thermal_printer_base_x = 103;
thermal_printer_base_y = 57;

//case_top_all();
case();
//lcd_display();

module case() {
    difference() {
        cube([case_x, case_y, case_z], center=is_center);
        translate([case_thickness,case_thickness,case_thickness])
            cube([case_x - case_thickness*2, case_y - case_thickness*2, case_z - case_thickness], center=is_center);
        
        #translate([(case_x - thermal_printer_base_x)/2,case_thickness,5])
            rotate([90,0,0])
                cube([thermal_printer_base_x, thermal_printer_base_y, case_thickness], is_center);
    }
}

module case_top_all() {
    case_top();
    case_top_border();
    //lcd_display_embedded();
    case_top_screwholes_embedded();
}

module case_top_screwholes_embedded() {
    screwhole_translate_y_start = printer_hole_translate_y + lcd_screen_y/2;
    #translate([(case_top_x/2 - screwhole_x), screwhole_translate_y_start + screwhole_y, case_top_z])
        screwhole_barrel();
    translate([(case_top_x/2 - screwhole_x), screwhole_translate_y_start - screwhole_y, case_top_z])
        screwhole_barrel();
    translate([(case_top_x/2 + screwhole_x), screwhole_translate_y_start + screwhole_y, case_top_z])
        screwhole_barrel();
    translate([(case_top_x/2 + screwhole_x), screwhole_translate_y_start - screwhole_y, case_top_z])
        screwhole_barrel();
}    

module screwhole_barrel() {
    is_center = true;
    outer_diameter = screwhole_radius * 3;
    inner_diameter = screwhole_radius;
    translate([0,0,screwhole_z/2])
        difference() {
            cylinder(screwhole_z, r= outer_diameter, center=is_center);
            cylinder(screwhole_z, r= inner_diameter, center=is_center);
        }
}

module case_top_border() {
    thickness = 3;
    difference() {
        translate([case_top_inset, case_top_inset, case_top_z])
            cube([case_top_x - case_top_inset*2, case_top_y - case_top_inset*2, case_top_thickness]);
        translate([case_top_inset+case_top_thickness, case_top_inset+case_top_thickness, case_top_z])
            cube([case_top_x - (case_top_inset*2 + case_top_thickness*2), case_top_y - (case_top_inset*2 + case_top_thickness*2), case_top_thickness]);

    }
}


module case_top() {
    difference() {
        cube([case_top_x, case_top_y, case_top_z]);
        translate([(case_top_x - lcd_screen_x)/2, printer_hole_translate_y, 0])
            printer_hole();
        #translate([(case_top_x)/2, button_hole_translate_y, 0])
            button_hole();
    }
}

module button_hole() {
    cylinder(case_top_z*2, r= button_radius, center=true);
}

module printer_hole() {
    cube([lcd_screen_x, lcd_screen_y, case_top_z]);
}

module lcd_display_embedded() {
    rotate([180,0,0])
        translate([(case_top_x-pcb_x)/2,-pcb_y + -printer_hole_translate_y + (pcb_y - lcd_screen_y)/2, -(pcb_z + lcd_screen_z)])
            lcd_display();
}
module lcd_display() {
    is_center = true;
    translate([pcb_x/2, pcb_y/2, pcb_z/2])
        difference() {
            union() {
                cube([pcb_x, pcb_y, pcb_z], center=is_center);
                translate([0,0,(lcd_screen_z + pcb_z) / 2])
                    cube([lcd_screen_x, lcd_screen_y, lcd_screen_z], center=is_center);
            }
            translate([screwhole_x, screwhole_y, 0])
                cylinder(h=pcb_z, r=screwhole_radius, center=is_center);
            translate([-screwhole_x, screwhole_y, 0])
                cylinder(h=pcb_z, r=screwhole_radius, center=is_center);
            translate([screwhole_x, -screwhole_y, 0])
                cylinder(h=pcb_z, r=screwhole_radius, center=is_center);
            translate([-screwhole_x, -screwhole_y, 0])
                cylinder(h=pcb_z, r=screwhole_radius, center=is_center);
        }
    
}
let vehicle, vehicle_reports = [];
const vehicleReg = $("#main-h3").attr("data-reg"),
    downloadBtn = $("#downloadPdfButton");

$.ajax({
    url: `http://omata.skyetechgroup.com/ajax/vehicle-reports/${vehicleReg}`,
    dataType: "json",
    success: function (data) {
        if (data.found) {
            vehicle = JSON.parse(data["vehicle"])[0].fields;
        }
        if (data.recent_reports) {
            vehicle_reports = JSON.parse(data.recent_reports).map(
                report => [report.fields.date, report.fields.time, report.fields.speed, report.fields.latitude, report.fields.longitude]
            );
            downloadBtn.html("<i class=\"fa fa-download\"></i> Download Reports")
            downloadBtn.attr("disabled", false);
        }
    }
})

const getImg64 = domId => {
    const c = document.createElement('canvas');
    const img = document.getElementById(domId);
    c.height = img.naturalHeight;
    c.width = img.naturalWidth;
    const ctx = c.getContext('2d');
    ctx.drawImage(img, 0, 0, c.width, c.height);
    return c.toDataURL();
};

function generateReportsPdf() {
    const logo64 = getImg64("logo");
    const doc = new jsPDF();

    doc.addImage(logo64, "PNG", 15, 15, 50, 20);

    doc.setFontSize(10);
    doc.text("Dalcom Kenya Limited", 150, 20);
    doc.text("P.O Box 17491-00100", 150, 25);
    doc.text("Upper Hill Gardens", 150, 30);
    doc.text("3rd Avenue, Block C-22", 150, 35);
    doc.text("Nairobi, Kenya.", 150, 40);

    doc.setFontSize(18);
    doc.text(`${reg}: HEADER DATA`, 15, 55);

    doc.rect(15, 58, 180, 5, "F");

    doc.setFontSize(15);
    doc.text("Header", 15, 70);

    doc.autoTable({
        startY: 75,
        body: [
            ["Vehicle Owner's Name:", vehicle.owner_name, "|", "Limiter Type:", vehicle.limiter_type],
            ["Vehicle Owner's ID:", vehicle.owner_id, "|", "Limiter Serial:", vehicle.limiter_serial],
            ["Vehicle Owner's Phone:", vehicle.owner_phone, "|", "Fitting Agent:", vehicle.fitting_agent],
            ["Vehicle Reg. Number:", vehicle.reg, "|", "Fitting Agent ID:", vehicle.fitting_agent_id],
            ["Vehicle Chassis No.:", vehicle.chassis_number, "|", "Agent's Location:", vehicle.fitting_agent_location],
            ["Vehicle Make & Model:", vehicle.make + vehicle.model, "|", "Agent's Email:", vehicle.fitting_agent_email],
            ["Fitting Technician:", vehicle.technician_name, "|", "Agent's Phone:", vehicle.fitting_agent_phone],
            ["Sacco Name:", vehicle.sacco_name, "|", "Business Reg:", vehicle.business_reg_no],
        ]
    });

    let finalY = doc.previousAutoTable.finalY;

    doc.text("Trip Data", 16, finalY + 15);

    doc.autoTable({
        startY: finalY + 20,
        head: [["Date", "Time", "Speed", "Latitude", "Longitude"]],
        body: vehicle_reports,
    });

    doc.save(`${reg}-${new Date().toLocaleString()}.pdf`);
};

downloadBtn.click(function () {
    generateReportsPdf();
    downloadBtn.attr("disabled", true);
});

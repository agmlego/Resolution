<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8">
        <title>IEEE 3D Printer Job Uploader</title>
        <link rel="stylesheet" type="text/css" href="default.css">
    </head>
    <body>
        <form enctype="multipart/form-data" action="save_file.py" method="post">
            <p>Please enter your name and either your phone number or your email address so we can contact you when your print job is done.</p>
            <table>
                <tr><td>Name:</td><td><input type="text" name="name"></td></tr>
                <tr><td>Email:</td><td><input type="text" name="email"></td></tr>
                <tr><td>Phone:</td><td><input type="text" name="phone"></td></tr>
            </table>
            <hr>
            <p>File (currently STL only): <input type="file" name="file"></p>
            <p>Material (currently available in the lab, make a comment below if you want something different):
            <div>
            %s
            </div>
            <hr class="bracket">
            <p>Slicer settings, which control how the model is "sliced", or converted into layers of instructions for the printer to run. If in doubt, leave these at the default settings.</p>
            <table>
                <tr><td><a class="description" title="The distance the printer drops the table for each new layer.&#10;&#13;This affects how well layers bond together, and the overall rigidity and resolution of the part.">Z-step (0.125-0.500mm)</a></td>
                    <td><input type="text" name="zstep" size=4 maxlength=5 value="0.25"></td></tr>
                <tr><td><a class="description" title="Of the interior volume of the part, how much should be solid plastic?">Fill %%</a></td>
                    <td><input type="text" name="fillp" size=4 maxlength=3 value="25"></td></tr>
                <tr><td><a class="description" title="Whether to build a support structure under overhangs.&#10;&#13;On the one hand, for larger models, this may be necessary to prevent collapse. On the other hand, the more support you use, the more plastic lab technicians need to pull off your part before it is finished, and the more plastic will need to be recycled. Use wisely.">Support?</a></td>
                    <td><input type="checkbox" name="support" value="true"></td></tr>
                <tr><td><a class="description" title="Number of lines used to make the perimeter of each layer.">Wall Lines</a></td>
                    <td><input type="text" name="wallnum" size=4 maxlength=1 value="3"><br></td></tr>
                <tr><td><a class="description" title="Minimum thickness a wall should be.">Wall Thickness (mm)</a></td>
                    <td><input type="text" name="wallthick" size=4 maxlength=5 value="0.595"></td></tr>
            </table>
            <hr>
            <p>Post-processing details, once the part has completed printing.</p>
            <p><a class="description" title="Should the lab technicians remove the raft and support material, or hand it over as-is fresh off the printer?">Cleanup?</a><input type="checkbox" name="cleanup" value="true"></p>
            <p><a class="description" title="Should the lab technicians bathe the part in acetone? This leaves a smooth, high-gloss finish on ABS plastic parts.">Acetone Bath?</a><input type="checkbox" name="acetone" value="true"></p>
            <hr>
            <p><input type="submit" value="Upload"></p>
            <p>Comments, questions, special instructions:<br>
                <textarea rows="4" cols="40" name="comments"></textarea></p>
        </form>
        <hr>
        <p>If you have any further questions, or any old parts or junk plastic (ABS or PLA only, please!), feel free to email us at <a href="mailto:ieee@mtu.edu?Subject=3D%%20Printer">our email address</a>, or drop by our lab in EERC 809.</p>
    </body>
</html>

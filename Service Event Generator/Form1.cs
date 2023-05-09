using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Text.RegularExpressions;
using Microsoft.VisualBasic;
using System.Windows.Controls;
using System.IO;
//using Smartsheet.API;
//using Smartsheet.Api.Models;

namespace Service_Event_Generator
{
    /// <summary>
    /// SERVICE EVENT GENERATOR
    /// Program built to accept agent input to create a professional Service Event to copy to Synapsys.
    /// 
    /// Features include:
    ///     * Toggling between Banks and CU
    ///     * Ability to automatically add "Thank you" to the end of each S/E
    ///     * Ability to copy the entire S/E or to copy the standard required fields individually
    ///     * Ability to clear the form and undo that action
    ///     * Alerting the agent when required fields are missing
    ///     * Formats account numbers and phone numbers in an easily readable format
    ///     * Ability to generate an email to the sups upon synapsys load fails (including sending tech error form)
    ///     * Stores agent settings (including their extension) and reloads them upon startup
    ///     
    /// Created by Lindsey Heinrichs and developed by Daniel Isaman for the JHA Call Center June 2021
    /// </summary>


    public partial class Form1 : Form
    {
        // GLOBAL VARIABLES
        // Location of settings file
        static string textPath = Path.GetDirectoryName(Application.ExecutablePath).ToString() + @"\..\..\SEGSettings.txt";

        // Variables to hold the input data
        string name = "";
        string acct = "";
        string phone = "";
        string card = "";
        string trans = "";
        string details = "";
        int refType = 1;
        int contType = 1;

        // Variable indicates whether the Undo button is visible (immediately after form has been cleared)
        bool undo = false;

        // Variables to store the user's settings choices
        bool thank = true;
        bool cu = false;
        string extension = "i.e. jha4321";

        // Variable to store the reference number label and choice
        string refLabel = "Account #";

        // Variable to determine whether the email function is on or off
        bool emailEnabled = true;



        // INITIALIZING THE FORM
        public Form1()
        {
            InitializeComponent();

            // Default upon opening is to assume bank (Customer, not Member) and to use "Thank you."
            lblCustomer.Text = "Customer Name*:";
            customerChoice.Checked = true;
            memberChoice.Checked = false;
            thankOnChoice.Checked = true;
            thankOffChoice.Checked = false;
            ref1.Text = "Account #";
            ref2.Text = "NetTeller ID";
            attnDetails.Visible = attnName.Visible = attnPhone.Visible = attnRef.Visible = false;
            lblMissing.Visible = false;

            if(!emailEnabled)
            {
                RemoveEmailOptions();
            }

            // Read the settings file and change the settings accordingly
            ReadSettings();
        }





        // METHODS TO HANDLE CHANGNING TEXT IN THE INPUT FIELDS
        private void txtName_TextChanged(object sender, EventArgs e)
        {
            // Change the built service event
            ChangeText();

            // If the text was not changed as a result of using Undo or Clear, set the Clear button to Clear
            if (txtName.Text != name && txtName.Text != "")
            {
                btnClear.Text = "CLEAR";
                toolTip1.SetToolTip(this.btnClear, "Clear the form");
                undo = false;
            }
        }

        private void txtAcct_TextChanged(object sender, EventArgs e)
        {
            // Change the built service event
            ChangeText();

            // If the text was not changed as a result of using Undo or Clear, set the Clear button to Clear
            if (txtAcct.Text != name && txtAcct.Text != "")
            {
                btnClear.Text = "CLEAR";
                toolTip1.SetToolTip(this.btnClear, "Clear the form");
                undo = false;
            }
        }

        private void txtPhone_TextChanged(object sender, EventArgs e)
        {
            // Change the built service event
            ChangeText();

            // If the text was not changed as a result of using Undo or Clear, set the Clear button to Clear
            if (txtPhone.Text != name && txtPhone.Text != "")
            {
                btnClear.Text = "CLEAR";
                toolTip1.SetToolTip(this.btnClear, "Clear the form");
                undo = false;
            }
        }

        private void txtCard_TextChanged(object sender, EventArgs e)
        {
            // Change the built service event
            ChangeText();

            // If the text was not changed as a result of using Undo or Clear, set the Clear button to Clear
            if (txtCard.Text != name && txtCard.Text != "")
            {
                btnClear.Text = "CLEAR";
                toolTip1.SetToolTip(this.btnClear, "Clear the form");
                undo = false;
            }
        }

        private void txtTrans_TextChanged(object sender, EventArgs e)
        {
            // Change the built service event
            ChangeText();

            // If the text was not changed as a result of using Undo or Clear, set the Clear button to Clear
            if (txtTrans.Text != name && txtTrans.Text != "")
            {
                btnClear.Text = "CLEAR";
                toolTip1.SetToolTip(this.btnClear, "Clear the form");
                undo = false;
            }
        }

        private void txtDetails_TextChanged(object sender, EventArgs e)
        {
            // Change the built service event
            ChangeText();

            // If the text was not changed as a result of using Undo or Clear, set the Clear button to Clear
            if (txtDetails.Text != name && txtDetails.Text != "")
            {
                btnClear.Text = "CLEAR";
                toolTip1.SetToolTip(this.btnClear, "Clear the form");
                undo = false;
            }
        }


        private void ChangeText()
        {
            // If everything has not just been cleared
            if (txtName.Text != "" || txtDetails.Text != "" || txtAcct.Text != "" || txtPhone.Text != "" || txtCard.Text != "" ||
                txtTrans.Text != "")
            {

                //Build the service event template
                string info = "";
                if (txtName.Text != "")
                {
                    if (cu)
                    {
                        info = $"Member: {txtName.Text}";
                    }
                    if (!cu)
                    {
                        info = $"Customer: {txtName.Text}";
                    }
                }

                if (txtDetails.Text != "")
                {
                    if(txtName.Text != "")
                    {
                        info += "\r\n\r\n";
                    }
                    info += $"{txtDetails.Text}";

                    if (thank)
                    {
                        info += " Thank you.";
                    }
                }


                if (txtAcct.Text != "")
                {
                    if (txtName.Text != "" || txtDetails.Text != "")
                    {
                        info += "\r\n\r\n";
                    }
                    // Special formatting for the account number to ensure it's only numbers, S, L, or hyphen
                    string aNum = "";
                    aNum = Regex.Replace(txtAcct.Text, "[^lLsS0-9-]", String.Empty);
                    info += $"{refLabel}: {aNum.ToUpper()}";
                }

                if (txtPhone.Text != "")
                {
                    // Format the phone number or email
                    string str = "";
                    if (contactP.Checked)
                    {
                        // Special formatting for the phone number before it is added
                        str = Regex.Replace(txtPhone.Text, "[^0-9+]", String.Empty);

                        if (!str.Contains("+"))
                        {
                            // If the phone number begins with a 1, remove the 1
                            if (str.Length != 0)
                            {
                                if (str.Substring(0, 1) == "1")
                                {
                                    str = str.Remove(0, 1);
                                }
                            }

                            // If the phone length is a 10-digit number, format it XXX-XXX-XXXX
                            if (str.Length == 10)
                            {
                                str = str.Substring(0, 3) + "-" + str.Substring(3, 3) + "-" + str.Substring(6, 4);
                            }
                        }
                        else
                        {
                            // FORMAT FOR INTERNATIONAL NUMBERS 
                            if (str.Length >= 11)
                            {
                                str = str.Substring(0, (str.Length - 10)) + " " + str.Substring((str.Length - 10), 3) + "-" +
                                    str.Substring((str.Length - 7), 3) + "-" + str.Substring((str.Length - 4), 4);
                            }
                        }
                    }
                    if (contactE.Checked)
                    {
                        // No limitations for email address
                        str = txtPhone.Text;
                    }

                    if (txtName.Text != "" || txtDetails.Text != "" || txtAcct.Text != "")
                    {
                        info += "\r\n";
                    }
                    if (contactP.Checked)
                    {
                        info += $"Phone #: {str}";
                    }
                    if (contactE.Checked)
                    {
                        info += $"Email: {str}";
                    }
                }


                //Depending on if additional info was input, add that to the template as well
                if (txtCard.Text != "")
                {
                    if (txtName.Text != "" || txtDetails.Text != "" || txtAcct.Text != "" || txtPhone.Text != "")
                    {
                        info += "\r\n";
                    }
                    info += $"Last 4 of card: {txtCard.Text}";
                }

                if (txtTrans.Text != "")
                {
                    if (txtName.Text != "" || txtDetails.Text != "" || txtAcct.Text != "" || 
                        txtPhone.Text != "" || txtCard.Text != "")
                    {
                        info += "\r\n\r\n";
                    }
                    info += $"Transactions: \r\n{txtTrans.Text}";
                }

                // Change the text that can be copied/pasted
                txtCopy.Text = info;
            }

            // If the text was changed because the form was cleared, also clear the template
            else
            {
                txtCopy.Text = "";
            }

            // If the update added text to a previously missing field, remove the red border
            SetAttention(0);
        }





        // METHODS TO HANDLE INDIVIDUAL FIELD COPY CLICKS
        private void copyName_Click(object sender, EventArgs e)
        {
            if (txtName.Text != "")
            {
                // Copy the caller's name to the clipboard (so they can paste it to required fields)
                Clipboard.SetText(txtName.Text);
            }
        }

        private void copyAcct_Click(object sender, EventArgs e)
        {
            if (txtAcct.Text != "")
            {
                // Remove any non-number characters
                string str = "";
                str = Regex.Replace(txtAcct.Text, "[^0-9]", String.Empty);

                // Copy the account number to the clipboard (so they can paste it to required fields)
                Clipboard.SetText(str);
            }
        }

        private void copyPhone_Click(object sender, EventArgs e)
        {
            if (txtPhone.Text != "")
            {
                // Remove any non-number characters
                string str = "";
                str = Regex.Replace(txtPhone.Text, "[^0-9]", String.Empty);

                // If the phone number begins with a 1, remove the 1
                if (str.Length != 0)
                {
                    if (str.Substring(0, 1) == "1")
                    {
                        str = str.Remove(0, 1);
                    }
                }

                // Copy the phone number to the clipboard (so they can paste it to required fields)
                Clipboard.SetText(str);
            }
        }

        private void copyDetails_Click(object sender, EventArgs e)
        {
            if (txtDetails.Text != "")
            {
                // Copy the call details to the clipboard (so they can paste it to required fields)
                Clipboard.SetText(txtDetails.Text);
            }
        }





        // METHODS TO HANDLE MAIN BUTTON CLICKS
        private void btnClear_Click(object sender, EventArgs e)
        {
            // If the button clicked says Undo, undo the last action and then change the button back to CHANGE
            if (undo)
            {
                // Restore the field values
                txtName.Text = name;
                txtAcct.Text = acct;
                txtPhone.Text = phone;
                txtCard.Text = card;
                txtTrans.Text = trans;
                txtDetails.Text = details;

                // Set the reference number radio buttons to the previous type
                switch(refType)
                {
                    case 2:
                        ref2.Checked = true;
                        break;
                    default:
                        ref1.Checked = true;
                        break;
                }

                // Set the contact radio buttons to the previous type
                switch (contType)
                {
                    case 2:
                        ref2.Checked = true;
                        break;
                    default:
                        ref1.Checked = true;
                        break;
                }

                // Change button text and toggle undo
                btnClear.Text = "CLEAR";
                toolTip1.SetToolTip(this.btnClear, "Clear the form");
                undo = false;
            }

            // If the button clicked says Clear, store the values, clear the form, and then change the button to UNDO
            else
            {
                // Store the current values
                name = txtName.Text;
                acct = txtAcct.Text;
                phone = txtPhone.Text;
                card = txtCard.Text;
                trans = txtTrans.Text;
                details = txtDetails.Text; 

                // Remember how the radio buttons were set
                if(ref2.Checked)
                {
                    refType = 2;
                }
                else
                {
                    refType = 1;
                }

                if (contactE.Checked)
                {
                    contType = 2;
                }
                else
                {
                    contType = 1;
                }

                // Only change the button to Undo if the form is not already blank
                if (txtName.Text != "" || txtDetails.Text != "" || txtAcct.Text != "" || txtPhone.Text != "" || txtCard.Text != "" ||
                txtTrans.Text != "")
                {
                    // Change button text and toggle undo
                    btnClear.Text = "UNDO";
                    toolTip1.SetToolTip(this.btnClear, "Undo the clearing of the form");
                    undo = true;
                }

                // Erase all input info from fields
                txtName.Text = txtAcct.Text = txtPhone.Text = txtCard.Text = txtTrans.Text = txtDetails.Text = txtCopy.Text = "";
                ref1.Checked = true;
                contactP.Checked = true;
            }
        }

        private void btnCopy_Click(object sender, EventArgs e)
        {
            // Copy the service event to the clipboard and alert the user to any missing info
            SetAttention(1);
            if (txtCopy.Text != "")
            {
                Clipboard.SetText(txtCopy.Text);
            }
        }

        private void btnEmail_Click(object sender, EventArgs e)
        {
            // Set the location for the input boxes
            int x = Left + (Width / 2) - 180;
            int y = Top + (Height / 2) - 100;

            // Ensure that user is alerted if required fields are not input
            SetAttention(1);

            // Customize dialog based on FI type
            string fiType = "Bank";
            string example = "Glacier Bank";

            // Generate an email to the sup inbox
            if (cu)
            {
                fiType = "CU";
                example = "Andrews Federal CU";
            }
            string fi = Interaction.InputBox($"What is the name of the {fiType}?", "Title", $"i.e. {example}", x, y);
            string ext = "";

            // Only continue to extension if bank name was not canceled
            // If it has not been saved in Settings, get the agent's extension
            if (fi != "")
            {
                if (extension != "i.e. jha4321" && extension != "")
                {
                    ext = extension;
                }
                else
                {
                    extension = "i.e. jha4321";
                    ext = Interaction.InputBox("What is your extension?", "Extension", extension, x, y);
                }
            }


            // Only continue if the extension was not canceled
            // See if the agent wants to submit a technical error form
            if (ext != "")
            {
                // Format the extension as jhaXXXX
                ext = Regex.Replace(ext, "[^0-9]", String.Empty);

                if (ext.Substring(0, 2) == "32")
                {
                    ext = ext.Remove(0, 2);
                }

                ext = "jha" + ext;

                DialogResult choice = MessageBox.Show("Do you need to submit a technical error form?", "Submit Error Form?",
                    MessageBoxButtons.YesNo);

                if (choice == DialogResult.Yes)
                {
                    if (cu)
                    {
                        System.Diagnostics.Process.Start(new System.Diagnostics.ProcessStartInfo("https://app.smartsheet.com/b/form/b09da0f620d04c45aeae3db44606d335") { UseShellExecute = true });
                    }
                    else
                    {
                        System.Diagnostics.Process.Start(new System.Diagnostics.ProcessStartInfo("https://app.smartsheet.com/b/form/01581776b2564281b36ba9fc96f213c8") { UseShellExecute = true });
                    }
                }
            }


            // Create the mailto: string
            string mailtoString = "mailto:";
            //if (cu)
            // {
            //    mailtoString += "jhaepicentersups@jackhenry.com";
            //}
            //else
            //{
            //    mailtoString += "JHABankingCenterSups@jackhenry.com";
            //}
            mailtoString += "JCCSupervisors@jackhenry.com";
            mailtoString += $"?subject=Service Event Needed For {fi}&body=";
            mailtoString += $"I was unable to send a service event for {fi}. Please submit the following:%0D%0A%0D%0A";
            mailtoString += txtCopy.Text;
            mailtoString += $"%0D%0A%0D%0ASent on behalf of {ext}";

            string myString = mailtoString.Replace(System.Environment.NewLine, "%0D%0A");

            // Only open email if procedure has not been canceled
            if (fi != "" && ext != "")
            {
                System.Diagnostics.Process.Start(myString);
            }
        }


        private void SetAttention(int n)
        {
            // If the text has been added, hide the red outline
            // If the COPY button has been clicked, outline in red any missing required fields
            switch (n)
            {
                case 1:
                    if (txtName.Text == "")
                    {
                        attnName.Visible = true;
                    }

                    if (txtAcct.Text == "")
                    {
                        attnRef.Visible = true;
                    }

                    if (txtPhone.Text == "")
                    {
                        attnPhone.Visible = true;
                    }

                    if (txtDetails.Text == "")
                    {
                        attnDetails.Visible = true;
                    }

                    if (txtName.Text == "" || txtAcct.Text == "" || txtPhone.Text == "" || txtDetails.Text == "")
                    {
                        lblMissing.Visible = true;
                    }
                    break;
                default:
                    if (txtName.Text != "")
                    {
                        attnName.Visible = false;
                    }

                    if (txtAcct.Text != "")
                    {
                        attnRef.Visible = false;
                    }

                    if (txtPhone.Text != "")
                    {
                        attnPhone.Visible = false;
                    }

                    if (txtDetails.Text != "")
                    {
                        attnDetails.Visible = false;
                    }

                    if (txtName.Text != "" && txtAcct.Text != "" && txtPhone.Text != "" && txtDetails.Text != "")
                    {
                        lblMissing.Visible = false;
                    }
                    break;
            }
        }





        // METHODS TO HANDLE RADIO BUTTON CHOICES
        private void ref1_CheckedChanged(object sender, EventArgs e)
        {
            setReferenceNumber(1);
        }

        private void ref2_CheckedChanged(object sender, EventArgs e)
        {
            setReferenceNumber(2);
        }

        private void contactP_CheckedChanged(object sender, EventArgs e)
        {
            ChangeText();
        }

        private void contactE_CheckedChanged(object sender, EventArgs e)
        {
            ChangeText();
        }


        private void setReferenceNumber(int n)
        {
            if (cu)
            {
                switch (n)
                {
                    case 2:
                        refLabel = "Loan #";
                        break;
                    default:
                        refLabel = "Member #";
                        break;
                }
            }
            else
            {
                switch (n)
                {
                    case 2:
                        refLabel = "NetTeller ID";
                        break;
                    default:
                        refLabel = "Account #";
                        break;
                }
            }

            ChangeText();
        }





        // METHODS TO HANDLE CHOICES MADE IN THE APP SETTINGS
        private void customerChoice_Click(object sender, EventArgs e)
        {
            // Changes to form label and template text to refer to the caller as "Customer" (for banks)
            cu = false;
            customerChoice.Checked = true;
            memberChoice.Checked = false;
            lblCustomer.Text = "Customer Name*:";
            ref1.Text = "Account #";
            ref2.Text = "NetTeller ID";
            ref1.Checked = true;
            refLabel = ref1.Text;
            ChangeText();

            // Remember the settings for the future
            WriteSettings();
        }

        private void memberChoice_Click(object sender, EventArgs e)
        {
            // Changes to form label and template text to refer to the caller as "Member" (for CU)
            cu = true;
            customerChoice.Checked = false;
            memberChoice.Checked = true;
            lblCustomer.Text = "Member Name*:";
            ref1.Text = "Member #";
            ref2.Text = "Loan #";
            ref1.Checked = true;
            refLabel = ref1.Text;
            ChangeText();

            // Remember the settings for the future
            WriteSettings();
        }

        private void thankOnChoice_Click(object sender, EventArgs e)
        {
            // Automatically adds "Thank you" to the end of the details in the template
            thank = true;
            thankOnChoice.Checked = true;
            thankOffChoice.Checked = false;
            ChangeText();

            // Remember the settings for the future
            WriteSettings();
        }

        private void thankOffChoice_Click(object sender, EventArgs e)
        {
            // Does not automatically add "Thank you" to the end of the details in the template
            thank = false;
            thankOnChoice.Checked = false;
            thankOffChoice.Checked = true;
            ChangeText();

            // Remember the settings for the future
            WriteSettings();
        }

        private void setExt_Click(object sender, EventArgs e)
        {
            // Set the location for the input boxes
            int x = Left + (Width / 2) - 180;
            int y = Top + (Height / 2) - 100;

            // Ask the agent for their extension
            string result = Interaction.InputBox("What is your extension?", "Extension", extension, x, y);
            if (result != "")
            {
                extension = result;
            }

            // Save the results
            WriteSettings();
        }





        // METHODS TO READ AND WRITE AGENT SETTINGS
        private void ReadSettings()
        {
            // Check if a .txt file exists. If so, read it and change the settings. If not, or on error, set and write the default settings
            // Open the streamreader
            try
            {
                StreamReader sr = new StreamReader(textPath);
                string line = sr.ReadLine();

                // If the first line is true, set the app for CUs. Otherwise, set is for banks.
                if (line == "True")
                {
                    cu = true;
                    customerChoice.Checked = false;
                    memberChoice.Checked = true;
                    lblCustomer.Text = "Member Name*:";
                    ref1.Text = "Member #";
                    ref2.Text = "Loan #";
                    ref1.Checked = true;
                    refLabel = ref1.Text;
                    ChangeText();
                }
                else
                {
                    cu = false;
                    customerChoice.Checked = true;
                    memberChoice.Checked = false;
                    lblCustomer.Text = "Customer Name*:";
                    ref1.Text = "Account #";
                    ref2.Text = "NetTeller ID";
                    ref1.Checked = true;
                    refLabel = ref1.Text;
                    ChangeText();
                }

                // If the second line is true, set the app to automatically add "Thank you." Otherwise turn this off.
                line = sr.ReadLine();
                if (line == "True")
                {
                    thank = true;
                    thankOnChoice.Checked = true;
                    thankOffChoice.Checked = false;
                    ChangeText();
                }
                else
                {
                    thank = false;
                    thankOnChoice.Checked = false;
                    thankOffChoice.Checked = true;
                    ChangeText();
                }

                // Set the third line as the extension
                extension = sr.ReadLine();

                // Close the streamreader
                sr.Close();
            }

            // On error or if no settings exist, set and save the default settings
            catch
            {
                cu = false;
                thank = true;
                extension = "i.e. jha4321";
                WriteSettings();
            }
        }

        private void WriteSettings()
        {
            // Rewrite the .txt file with the current settings. If a file does not exist, create one.
            //Open the FileStream and writer
            StreamWriter sw = new StreamWriter(textPath, false);

            //Write to memory
            sw.WriteLine(cu.ToString());
            sw.WriteLine(thank.ToString());
            sw.WriteLine(extension);

            //Close the streamwriter
            sw.Close();
        }





        // METHOD TO MANAGE THE SIZE OF THE FORM
        private void Form1_Resize(object sender, EventArgs e)
        {
            // Only create the size restrictions if the fmorm is not minimized
            if (this.WindowState != FormWindowState.Minimized)
            {
                // Adjusts the width to account for the scrollbar if the height decreases
                if (Height < 859)
                {
                    Width = 506;
                }
                else
                {
                    Width = 487;
                }
            }
        }





        // METHOD TO REMOVE THE EMAIL OPTION
        private void RemoveEmailOptions()
        {
            setExt.Visible = false;
            btnEmail.Visible = false;
            // Button length = 215
            // Space between = 17
            btnCopy.Width = 215;
            btnClear.Width = 215;
            btnClear.Location = new Point(244,770);
        }
    }
}

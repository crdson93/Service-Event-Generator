
namespace Service_Event_Generator
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.label1 = new System.Windows.Forms.Label();
            this.lblCustomer = new System.Windows.Forms.Label();
            this.btnClear = new System.Windows.Forms.Button();
            this.txtName = new System.Windows.Forms.TextBox();
            this.txtAcct = new System.Windows.Forms.TextBox();
            this.lblAcct = new System.Windows.Forms.Label();
            this.txtPhone = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.txtCard = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.txtTrans = new System.Windows.Forms.TextBox();
            this.label7 = new System.Windows.Forms.Label();
            this.txtDetails = new System.Windows.Forms.TextBox();
            this.label8 = new System.Windows.Forms.Label();
            this.txtCopy = new System.Windows.Forms.TextBox();
            this.label9 = new System.Windows.Forms.Label();
            this.btnCopy = new System.Windows.Forms.Button();
            this.label6 = new System.Windows.Forms.Label();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.settingsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.referToCallerAsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.customerChoice = new System.Windows.Forms.ToolStripMenuItem();
            this.memberChoice = new System.Windows.Forms.ToolStripMenuItem();
            this.thankYouToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.thankOnChoice = new System.Windows.Forms.ToolStripMenuItem();
            this.thankOffChoice = new System.Windows.Forms.ToolStripMenuItem();
            this.setExt = new System.Windows.Forms.ToolStripMenuItem();
            this.copyName = new System.Windows.Forms.Label();
            this.copyAcct = new System.Windows.Forms.Label();
            this.copyPhone = new System.Windows.Forms.Label();
            this.ref2 = new System.Windows.Forms.RadioButton();
            this.ref1 = new System.Windows.Forms.RadioButton();
            this.attnDetails = new System.Windows.Forms.Panel();
            this.attnName = new System.Windows.Forms.Panel();
            this.attnRef = new System.Windows.Forms.Panel();
            this.attnPhone = new System.Windows.Forms.Panel();
            this.lblMissing = new System.Windows.Forms.Label();
            this.panel1 = new System.Windows.Forms.Panel();
            this.copyDetails = new System.Windows.Forms.Label();
            this.btnEmail = new System.Windows.Forms.Button();
            this.contactE = new System.Windows.Forms.RadioButton();
            this.contactP = new System.Windows.Forms.RadioButton();
            this.panel2 = new System.Windows.Forms.Panel();
            this.panel3 = new System.Windows.Forms.Panel();
            this.toolTip1 = new System.Windows.Forms.ToolTip(this.components);
            this.menuStrip1.SuspendLayout();
            this.panel2.SuspendLayout();
            this.panel3.SuspendLayout();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Arial Black", 20F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.label1.Location = new System.Drawing.Point(45, 29);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(381, 38);
            this.label1.TabIndex = 0;
            this.label1.Text = "Service Event Generator";
            // 
            // lblCustomer
            // 
            this.lblCustomer.AutoSize = true;
            this.lblCustomer.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblCustomer.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.lblCustomer.Location = new System.Drawing.Point(45, 79);
            this.lblCustomer.Name = "lblCustomer";
            this.lblCustomer.Size = new System.Drawing.Size(130, 19);
            this.lblCustomer.TabIndex = 1;
            this.lblCustomer.Text = "Customer Name*:";
            // 
            // btnClear
            // 
            this.btnClear.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.btnClear.Cursor = System.Windows.Forms.Cursors.Hand;
            this.btnClear.Font = new System.Drawing.Font("Arial Black", 16F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnClear.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(26)))), ((int)(((byte)(54)))), ((int)(((byte)(104)))));
            this.btnClear.Location = new System.Drawing.Point(202, 770);
            this.btnClear.Name = "btnClear";
            this.btnClear.Size = new System.Drawing.Size(175, 38);
            this.btnClear.TabIndex = 7;
            this.btnClear.Text = "CLEAR";
            this.toolTip1.SetToolTip(this.btnClear, "Clear the form");
            this.btnClear.UseVisualStyleBackColor = false;
            this.btnClear.Click += new System.EventHandler(this.btnClear_Click);
            // 
            // txtName
            // 
            this.txtName.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtName.Location = new System.Drawing.Point(67, 100);
            this.txtName.Name = "txtName";
            this.txtName.Size = new System.Drawing.Size(362, 27);
            this.txtName.TabIndex = 0;
            this.txtName.TextChanged += new System.EventHandler(this.txtName_TextChanged);
            // 
            // txtAcct
            // 
            this.txtAcct.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtAcct.Location = new System.Drawing.Point(67, 181);
            this.txtAcct.Name = "txtAcct";
            this.txtAcct.Size = new System.Drawing.Size(362, 27);
            this.txtAcct.TabIndex = 1;
            this.txtAcct.TextChanged += new System.EventHandler(this.txtAcct_TextChanged);
            // 
            // lblAcct
            // 
            this.lblAcct.AutoSize = true;
            this.lblAcct.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblAcct.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.lblAcct.Location = new System.Drawing.Point(18, 6);
            this.lblAcct.Name = "lblAcct";
            this.lblAcct.Size = new System.Drawing.Size(149, 19);
            this.lblAcct.TabIndex = 4;
            this.lblAcct.Text = "Reference Number*:";
            // 
            // txtPhone
            // 
            this.txtPhone.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtPhone.Location = new System.Drawing.Point(67, 262);
            this.txtPhone.Name = "txtPhone";
            this.txtPhone.Size = new System.Drawing.Size(362, 27);
            this.txtPhone.TabIndex = 2;
            this.txtPhone.TextChanged += new System.EventHandler(this.txtPhone_TextChanged);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.label4.Location = new System.Drawing.Point(15, 4);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(105, 19);
            this.label4.TabIndex = 6;
            this.label4.Text = "Contact Info*:";
            // 
            // txtCard
            // 
            this.txtCard.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtCard.Location = new System.Drawing.Point(67, 321);
            this.txtCard.Name = "txtCard";
            this.txtCard.Size = new System.Drawing.Size(362, 27);
            this.txtCard.TabIndex = 3;
            this.txtCard.TextChanged += new System.EventHandler(this.txtCard_TextChanged);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.label5.Location = new System.Drawing.Point(45, 300);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(188, 19);
            this.label5.TabIndex = 8;
            this.label5.Text = "Last 4 Digits of Debit Card:";
            // 
            // txtTrans
            // 
            this.txtTrans.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtTrans.Location = new System.Drawing.Point(67, 378);
            this.txtTrans.Multiline = true;
            this.txtTrans.Name = "txtTrans";
            this.txtTrans.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.txtTrans.Size = new System.Drawing.Size(362, 62);
            this.txtTrans.TabIndex = 4;
            this.txtTrans.TextChanged += new System.EventHandler(this.txtTrans_TextChanged);
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.label7.Location = new System.Drawing.Point(45, 357);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(312, 19);
            this.label7.TabIndex = 12;
            this.label7.Text = "Transactions (Date, Amount, and Merchant):";
            // 
            // txtDetails
            // 
            this.txtDetails.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtDetails.Location = new System.Drawing.Point(67, 469);
            this.txtDetails.Multiline = true;
            this.txtDetails.Name = "txtDetails";
            this.txtDetails.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.txtDetails.Size = new System.Drawing.Size(362, 83);
            this.txtDetails.TabIndex = 5;
            this.txtDetails.TextChanged += new System.EventHandler(this.txtDetails_TextChanged);
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label8.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.label8.Location = new System.Drawing.Point(45, 448);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(143, 19);
            this.label8.TabIndex = 14;
            this.label8.Text = "Reason for Calling*:";
            // 
            // txtCopy
            // 
            this.txtCopy.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtCopy.Location = new System.Drawing.Point(12, 626);
            this.txtCopy.Multiline = true;
            this.txtCopy.Name = "txtCopy";
            this.txtCopy.ReadOnly = true;
            this.txtCopy.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.txtCopy.Size = new System.Drawing.Size(447, 130);
            this.txtCopy.TabIndex = 16;
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label9.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.label9.Location = new System.Drawing.Point(12, 604);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(199, 19);
            this.label9.TabIndex = 17;
            this.label9.Text = "Copy and paste to Synapsys";
            // 
            // btnCopy
            // 
            this.btnCopy.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.btnCopy.Cursor = System.Windows.Forms.Cursors.Hand;
            this.btnCopy.Font = new System.Drawing.Font("Arial Black", 16F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnCopy.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(26)))), ((int)(((byte)(54)))), ((int)(((byte)(104)))));
            this.btnCopy.Location = new System.Drawing.Point(12, 770);
            this.btnCopy.Name = "btnCopy";
            this.btnCopy.Size = new System.Drawing.Size(175, 38);
            this.btnCopy.TabIndex = 6;
            this.btnCopy.Text = "COPY";
            this.toolTip1.SetToolTip(this.btnCopy, "Copy S/E");
            this.btnCopy.UseVisualStyleBackColor = false;
            this.btnCopy.Click += new System.EventHandler(this.btnCopy_Click);
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Calibri", 10F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.label6.Location = new System.Drawing.Point(13, 555);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(321, 17);
            this.label6.TabIndex = 18;
            this.label6.Text = "*Required for any Service Events going back to the bank";
            // 
            // menuStrip1
            // 
            this.menuStrip1.BackColor = System.Drawing.SystemColors.Control;
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.settingsToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(471, 24);
            this.menuStrip1.TabIndex = 19;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // settingsToolStripMenuItem
            // 
            this.settingsToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.referToCallerAsToolStripMenuItem,
            this.thankYouToolStripMenuItem,
            this.setExt});
            this.settingsToolStripMenuItem.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.settingsToolStripMenuItem.Name = "settingsToolStripMenuItem";
            this.settingsToolStripMenuItem.Size = new System.Drawing.Size(61, 20);
            this.settingsToolStripMenuItem.Text = "Settings";
            // 
            // referToCallerAsToolStripMenuItem
            // 
            this.referToCallerAsToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.customerChoice,
            this.memberChoice});
            this.referToCallerAsToolStripMenuItem.Name = "referToCallerAsToolStripMenuItem";
            this.referToCallerAsToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.referToCallerAsToolStripMenuItem.Text = "Financial Institution";
            // 
            // customerChoice
            // 
            this.customerChoice.Name = "customerChoice";
            this.customerChoice.Size = new System.Drawing.Size(141, 22);
            this.customerChoice.Text = "Bank";
            this.customerChoice.Click += new System.EventHandler(this.customerChoice_Click);
            // 
            // memberChoice
            // 
            this.memberChoice.Name = "memberChoice";
            this.memberChoice.Size = new System.Drawing.Size(141, 22);
            this.memberChoice.Text = "Credit Union";
            this.memberChoice.Click += new System.EventHandler(this.memberChoice_Click);
            // 
            // thankYouToolStripMenuItem
            // 
            this.thankYouToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.thankOnChoice,
            this.thankOffChoice});
            this.thankYouToolStripMenuItem.Name = "thankYouToolStripMenuItem";
            this.thankYouToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.thankYouToolStripMenuItem.Text = "Auto Thank You";
            // 
            // thankOnChoice
            // 
            this.thankOnChoice.Name = "thankOnChoice";
            this.thankOnChoice.Size = new System.Drawing.Size(91, 22);
            this.thankOnChoice.Text = "On";
            this.thankOnChoice.Click += new System.EventHandler(this.thankOnChoice_Click);
            // 
            // thankOffChoice
            // 
            this.thankOffChoice.Name = "thankOffChoice";
            this.thankOffChoice.Size = new System.Drawing.Size(91, 22);
            this.thankOffChoice.Text = "Off";
            this.thankOffChoice.Click += new System.EventHandler(this.thankOffChoice_Click);
            // 
            // setExt
            // 
            this.setExt.Name = "setExt";
            this.setExt.Size = new System.Drawing.Size(180, 22);
            this.setExt.Text = "Set Extension";
            this.setExt.Click += new System.EventHandler(this.setExt_Click);
            // 
            // copyName
            // 
            this.copyName.AutoSize = true;
            this.copyName.Cursor = System.Windows.Forms.Cursors.Hand;
            this.copyName.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Underline, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.copyName.ForeColor = System.Drawing.Color.SkyBlue;
            this.copyName.Location = new System.Drawing.Point(389, 79);
            this.copyName.Name = "copyName";
            this.copyName.Size = new System.Drawing.Size(40, 17);
            this.copyName.TabIndex = 20;
            this.copyName.Text = "Copy";
            this.toolTip1.SetToolTip(this.copyName, "Copy customer name");
            this.copyName.Click += new System.EventHandler(this.copyName_Click);
            // 
            // copyAcct
            // 
            this.copyAcct.AutoSize = true;
            this.copyAcct.Cursor = System.Windows.Forms.Cursors.Hand;
            this.copyAcct.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Underline, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.copyAcct.ForeColor = System.Drawing.Color.SkyBlue;
            this.copyAcct.Location = new System.Drawing.Point(389, 160);
            this.copyAcct.Name = "copyAcct";
            this.copyAcct.Size = new System.Drawing.Size(40, 17);
            this.copyAcct.TabIndex = 21;
            this.copyAcct.Text = "Copy";
            this.toolTip1.SetToolTip(this.copyAcct, "Copy reference number");
            this.copyAcct.Click += new System.EventHandler(this.copyAcct_Click);
            // 
            // copyPhone
            // 
            this.copyPhone.AutoSize = true;
            this.copyPhone.Cursor = System.Windows.Forms.Cursors.Hand;
            this.copyPhone.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Underline, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.copyPhone.ForeColor = System.Drawing.Color.SkyBlue;
            this.copyPhone.Location = new System.Drawing.Point(389, 241);
            this.copyPhone.Name = "copyPhone";
            this.copyPhone.Size = new System.Drawing.Size(40, 17);
            this.copyPhone.TabIndex = 22;
            this.copyPhone.Text = "Copy";
            this.toolTip1.SetToolTip(this.copyPhone, "Copy contact info");
            this.copyPhone.Click += new System.EventHandler(this.copyPhone_Click);
            // 
            // ref2
            // 
            this.ref2.AutoSize = true;
            this.ref2.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.ref2.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.ref2.Location = new System.Drawing.Point(150, 24);
            this.ref2.Name = "ref2";
            this.ref2.Size = new System.Drawing.Size(94, 17);
            this.ref2.TabIndex = 26;
            this.ref2.Text = "NetTeller ID";
            this.ref2.UseVisualStyleBackColor = true;
            this.ref2.CheckedChanged += new System.EventHandler(this.ref2_CheckedChanged);
            // 
            // ref1
            // 
            this.ref1.AutoSize = true;
            this.ref1.Checked = true;
            this.ref1.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.ref1.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.ref1.Location = new System.Drawing.Point(40, 24);
            this.ref1.Name = "ref1";
            this.ref1.Size = new System.Drawing.Size(84, 17);
            this.ref1.TabIndex = 25;
            this.ref1.TabStop = true;
            this.ref1.Text = "Account #";
            this.ref1.UseVisualStyleBackColor = true;
            this.ref1.CheckedChanged += new System.EventHandler(this.ref1_CheckedChanged);
            // 
            // attnDetails
            // 
            this.attnDetails.BackColor = System.Drawing.Color.Red;
            this.attnDetails.Location = new System.Drawing.Point(65, 467);
            this.attnDetails.Name = "attnDetails";
            this.attnDetails.Size = new System.Drawing.Size(366, 87);
            this.attnDetails.TabIndex = 28;
            // 
            // attnName
            // 
            this.attnName.BackColor = System.Drawing.Color.Red;
            this.attnName.Location = new System.Drawing.Point(65, 98);
            this.attnName.Name = "attnName";
            this.attnName.Size = new System.Drawing.Size(366, 31);
            this.attnName.TabIndex = 29;
            // 
            // attnRef
            // 
            this.attnRef.BackColor = System.Drawing.Color.Red;
            this.attnRef.Location = new System.Drawing.Point(65, 179);
            this.attnRef.Name = "attnRef";
            this.attnRef.Size = new System.Drawing.Size(366, 31);
            this.attnRef.TabIndex = 30;
            // 
            // attnPhone
            // 
            this.attnPhone.BackColor = System.Drawing.Color.Red;
            this.attnPhone.Location = new System.Drawing.Point(65, 260);
            this.attnPhone.Name = "attnPhone";
            this.attnPhone.Size = new System.Drawing.Size(366, 31);
            this.attnPhone.TabIndex = 31;
            // 
            // lblMissing
            // 
            this.lblMissing.AutoSize = true;
            this.lblMissing.Font = new System.Drawing.Font("Calibri", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblMissing.ForeColor = System.Drawing.Color.Red;
            this.lblMissing.Location = new System.Drawing.Point(278, 604);
            this.lblMissing.Name = "lblMissing";
            this.lblMissing.Size = new System.Drawing.Size(181, 19);
            this.lblMissing.TabIndex = 32;
            this.lblMissing.Text = "-MISSING INFORMATION-";
            // 
            // panel1
            // 
            this.panel1.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.panel1.Location = new System.Drawing.Point(60, 585);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(350, 3);
            this.panel1.TabIndex = 33;
            // 
            // copyDetails
            // 
            this.copyDetails.AutoSize = true;
            this.copyDetails.Cursor = System.Windows.Forms.Cursors.Hand;
            this.copyDetails.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Underline, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.copyDetails.ForeColor = System.Drawing.Color.SkyBlue;
            this.copyDetails.Location = new System.Drawing.Point(389, 448);
            this.copyDetails.Name = "copyDetails";
            this.copyDetails.Size = new System.Drawing.Size(40, 17);
            this.copyDetails.TabIndex = 34;
            this.copyDetails.Text = "Copy";
            this.toolTip1.SetToolTip(this.copyDetails, "Copy reason for calling");
            this.copyDetails.Click += new System.EventHandler(this.copyDetails_Click);
            // 
            // btnEmail
            // 
            this.btnEmail.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.btnEmail.BackgroundImage = global::Service_Event_Generator.Properties.Resources.Email;
            this.btnEmail.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom;
            this.btnEmail.Cursor = System.Windows.Forms.Cursors.Hand;
            this.btnEmail.Font = new System.Drawing.Font("Arial Black", 16F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnEmail.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(26)))), ((int)(((byte)(54)))), ((int)(((byte)(104)))));
            this.btnEmail.Location = new System.Drawing.Point(392, 770);
            this.btnEmail.Name = "btnEmail";
            this.btnEmail.Size = new System.Drawing.Size(65, 38);
            this.btnEmail.TabIndex = 35;
            this.toolTip1.SetToolTip(this.btnEmail, "Email S/E to supervisors");
            this.btnEmail.UseVisualStyleBackColor = false;
            this.btnEmail.Click += new System.EventHandler(this.btnEmail_Click);
            // 
            // contactE
            // 
            this.contactE.AutoSize = true;
            this.contactE.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.contactE.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.contactE.Location = new System.Drawing.Point(147, 24);
            this.contactE.Name = "contactE";
            this.contactE.Size = new System.Drawing.Size(104, 17);
            this.contactE.TabIndex = 37;
            this.contactE.Text = "Email Address";
            this.contactE.UseVisualStyleBackColor = true;
            this.contactE.CheckedChanged += new System.EventHandler(this.contactE_CheckedChanged);
            // 
            // contactP
            // 
            this.contactP.AutoSize = true;
            this.contactP.Checked = true;
            this.contactP.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.contactP.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.contactP.Location = new System.Drawing.Point(37, 24);
            this.contactP.Name = "contactP";
            this.contactP.Size = new System.Drawing.Size(73, 17);
            this.contactP.TabIndex = 36;
            this.contactP.TabStop = true;
            this.contactP.Text = "Phone #";
            this.contactP.UseVisualStyleBackColor = true;
            this.contactP.CheckedChanged += new System.EventHandler(this.contactP_CheckedChanged);
            // 
            // panel2
            // 
            this.panel2.Controls.Add(this.contactE);
            this.panel2.Controls.Add(this.contactP);
            this.panel2.Controls.Add(this.label4);
            this.panel2.Location = new System.Drawing.Point(30, 215);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(272, 45);
            this.panel2.TabIndex = 38;
            // 
            // panel3
            // 
            this.panel3.Controls.Add(this.ref2);
            this.panel3.Controls.Add(this.ref1);
            this.panel3.Controls.Add(this.lblAcct);
            this.panel3.Location = new System.Drawing.Point(27, 132);
            this.panel3.Name = "panel3";
            this.panel3.Size = new System.Drawing.Size(254, 44);
            this.panel3.TabIndex = 39;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoScroll = true;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(26)))), ((int)(((byte)(54)))), ((int)(((byte)(104)))));
            this.ClientSize = new System.Drawing.Size(471, 820);
            this.Controls.Add(this.panel3);
            this.Controls.Add(this.panel2);
            this.Controls.Add(this.btnEmail);
            this.Controls.Add(this.copyDetails);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.lblMissing);
            this.Controls.Add(this.copyPhone);
            this.Controls.Add(this.copyAcct);
            this.Controls.Add(this.copyName);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.btnCopy);
            this.Controls.Add(this.label9);
            this.Controls.Add(this.txtCopy);
            this.Controls.Add(this.txtDetails);
            this.Controls.Add(this.label8);
            this.Controls.Add(this.txtTrans);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.txtCard);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.txtPhone);
            this.Controls.Add(this.txtAcct);
            this.Controls.Add(this.btnClear);
            this.Controls.Add(this.lblCustomer);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.menuStrip1);
            this.Controls.Add(this.attnDetails);
            this.Controls.Add(this.txtName);
            this.Controls.Add(this.attnPhone);
            this.Controls.Add(this.attnRef);
            this.Controls.Add(this.attnName);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MainMenuStrip = this.menuStrip1;
            this.MaximizeBox = false;
            this.MaximumSize = new System.Drawing.Size(506, 859);
            this.MinimumSize = new System.Drawing.Size(487, 360);
            this.Name = "Form1";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Service Event Generator";
            this.Resize += new System.EventHandler(this.Form1_Resize);
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.panel2.ResumeLayout(false);
            this.panel2.PerformLayout();
            this.panel3.ResumeLayout(false);
            this.panel3.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label lblCustomer;
        private System.Windows.Forms.Button btnClear;
        private System.Windows.Forms.TextBox txtName;
        private System.Windows.Forms.TextBox txtAcct;
        private System.Windows.Forms.Label lblAcct;
        private System.Windows.Forms.TextBox txtPhone;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox txtCard;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox txtTrans;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox txtDetails;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.TextBox txtCopy;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Button btnCopy;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem settingsToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem referToCallerAsToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem customerChoice;
        private System.Windows.Forms.ToolStripMenuItem memberChoice;
        private System.Windows.Forms.ToolStripMenuItem thankYouToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem thankOnChoice;
        private System.Windows.Forms.ToolStripMenuItem thankOffChoice;
        private System.Windows.Forms.Label copyName;
        private System.Windows.Forms.Label copyAcct;
        private System.Windows.Forms.Label copyPhone;
        private System.Windows.Forms.RadioButton ref2;
        private System.Windows.Forms.RadioButton ref1;
        private System.Windows.Forms.Panel attnDetails;
        private System.Windows.Forms.Panel attnName;
        private System.Windows.Forms.Panel attnRef;
        private System.Windows.Forms.Panel attnPhone;
        private System.Windows.Forms.Label lblMissing;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Label copyDetails;
        private System.Windows.Forms.Button btnEmail;
        private System.Windows.Forms.RadioButton contactE;
        private System.Windows.Forms.RadioButton contactP;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.Panel panel3;
        private System.Windows.Forms.ToolStripMenuItem setExt;
        private System.Windows.Forms.ToolTip toolTip1;
    }
}


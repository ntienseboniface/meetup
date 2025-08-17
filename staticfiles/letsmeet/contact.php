<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

// Require PHPMailer files
require 'PHPMailer/src/Exception.php';
require 'PHPMailer/src/PHPMailer.php';
require 'PHPMailer/src/SMTP.php';

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize form data
    $first_name = htmlspecialchars($_POST['first_name']);
    $email = htmlspecialchars($_POST['email']);
    $phone = htmlspecialchars($_POST['phone']);
    $subject = htmlspecialchars($_POST['subject']);
    $message = htmlspecialchars($_POST['message']);

    // Create a new PHPMailer instance
    $mail = new PHPMailer(true);

    try {
        // Server settings
        $mail->isSMTP();
        $mail->Host = 'smtp.babalawanempowerment.org'; // e.g. smtp.gmail.com
        $mail->SMTPAuth = true;
        $mail->Username = 'info@babalawanempowerment.org'; // Replace with your email
        $mail->Password = '@Babalawan@123'; // Replace with your password or app password
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS; // Or PHPMailer::ENCRYPTION_SMTPS
        $mail->Port = 465; // 465 for SSL

        // Recipients
        $mail->setFrom($email, $first_name);
        $mail->addAddress('info@babalawanempowerment.org', 'Baba Lawan Empowerment Initiative');

        // Content
        $mail->isHTML(true);
        $mail->Subject = "New Contact Message: $subject";
        $mail->Body = "
            <h3>New Contact Submission</h3>
            <p><strong>Name:</strong> $first_name</p>
            <p><strong>Email:</strong> $email</p>
            <p><strong>Phone:</strong> $phone</p>
            <p><strong>Subject:</strong> $subject</p>
            <p><strong>Message:</strong><br>$message</p>
        ";

        $mail->AltBody = "Name: $first_name\nEmail: $email\nPhone: $phone\nSubject: $subject\nMessage:\n$message";

        $mail->send();
        echo "<script>alert('Message sent successfully!'); window.history.back();</script>";
    } catch (Exception $e) {
        echo "<script>alert('Message could not be sent. Error: {$mail->ErrorInfo}'); window.history.back();</script>";
    }
}
?>
